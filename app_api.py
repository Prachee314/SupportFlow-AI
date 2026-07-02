from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.graph import app
from src.agents import resolution_node
from queue_store import (
    setup_queue_db,
    enqueue_ticket,
    update_ticket_status,
    get_next_pending_ticket,
    get_queue_counts,
    generate_thread_id,
    format_ticket_id,
    get_ticket_info,
)

api = FastAPI(
    title="Agentic Customer Support API"
)

setup_queue_db()


class TicketRequest(BaseModel):
    customer_name: str
    customer_email: str
    query: str
    thread_id: Optional[str] = None


class TicketReviewRequest(BaseModel):
    thread_id: str
    approved: bool
    feedback: Optional[str] = ""
    edited_response: str


@api.get("/")
def home():
    return {
        "message": "Agentic Customer Support API Running"
    }


@api.get("/health")
def health():
    return {
        "status": "healthy"
    }


@api.get("/ticket/state/{thread_id}")
def get_ticket_state(thread_id: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = app.get_state(config)

    if not state.values:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket = get_ticket_info(thread_id)

    return {
        "ticket": ticket,
        "state": state.values
    }


@api.get("/ticket/next")
def get_next_ticket():
    thread_id = get_next_pending_ticket()

    if thread_id is None:
        return {
            "status": "empty",
            "thread_id": None,
            "data": None
        }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    state = app.get_state(config)

    if not state.values:
        update_ticket_status(thread_id, "rejected")
        raise HTTPException(
            status_code=404,
            detail=f"Queued ticket {thread_id} has no graph state"
        )

    ticket = get_ticket_info(thread_id)

    return {
        "status": "found",
        "ticket": ticket,
        "data": state.values
    }


@api.get("/ticket/queue/counts")
def queue_counts():
    return get_queue_counts()


@api.post("/ticket/create")
def create_ticket(request: TicketRequest):

    # Generate thread_id if not provided (new ticket),
    # otherwise reuse the existing one (continuing ticket).
    if request.thread_id is None:
        thread_id = generate_thread_id()
    else:
        thread_id = request.thread_id

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    existing_state = app.get_state(config)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"text": request.query, "submitted_at": now}
    
    conversation_entry = {
    "role": "customer",
    "text": request.query,
    "submitted_at": now
}
    
    is_new_thread = not existing_state.values
    is_paused = bool(existing_state.next) and "human_review" in existing_state.next

    if is_new_thread:
        app.invoke(
            {
                "customer_query": request.query,
                "query_history": [new_entry],
                "conversation_history": [conversation_entry]
            },
            config
        )
        enqueue_ticket(
            thread_id,
            request.customer_name,
            request.customer_email
        )

    elif is_paused:
        history = list(existing_state.values.get("query_history", []))
        history.append(new_entry)
        
        conversation = list(
        existing_state.values.get(
        "conversation_history",
        []
    )
)
        conversation.append(conversation_entry)

        working_state = dict(existing_state.values)
        working_state["customer_query"] = request.query
        working_state["query_history"] = history
        working_state["conversation_history"] = conversation
        working_state["supervisor_feedback"] = None

        new_draft = resolution_node(working_state)["draft_response"]

        app.update_state(
            config,
            {
                "customer_query": request.query,
                "query_history": history,
                "conversation_history": conversation,
                "draft_response": new_draft
            }
        )

    else:
        history = list(existing_state.values.get("query_history", []))
        history.append(new_entry)
        
        conversation = list(
        existing_state.values.get(
        "conversation_history",
        []
    )
)

        conversation.append(conversation_entry)
        app.invoke(
            {
                "customer_query": request.query,
                "query_history": history,
                "conversation_history": [conversation_entry]
            },
            config
        )
        update_ticket_status(thread_id, "pending_review")

    state = app.get_state(config)

    print("=" * 50)
    print("THREAD ID:", thread_id)
    print("STATE VALUES:", state.values)
    print("=" * 50)

    return {
        "status": "waiting_for_review",
        "ticket_id": format_ticket_id(thread_id),
        "thread_id": thread_id,
        "data": state.values
    }


@api.post("/ticket/review")
def review_ticket(request: TicketReviewRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    state = app.get_state(config)

    if not state.values:
        raise HTTPException(
            status_code=404,
            detail="Ticket thread not found"
        )

    app.update_state(
        config,
        {
            "supervisor_approved": request.approved,
            "supervisor_feedback": request.feedback,
            "draft_response": request.edited_response
        },
        as_node="human_review"
    )

    app.invoke(None, config)

    final_state = app.get_state(config)
    conversation = list(
    final_state.values.get(
        "conversation_history",
        []
    )
)
    is_paused_for_review = bool(final_state.next) and "human_review" in final_state.next
    

    if is_paused_for_review:
        status = "pending_review"
        update_ticket_status(request.thread_id, "pending_review")
    elif request.approved:
        conversation.append(
        {
            "role": "support",
            "text": request.edited_response,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

        app.update_state(
        config,
        {
            "conversation_history": conversation
        }
    )
        final_state = app.get_state(config)
        status = "completed"

        update_ticket_status(
        request.thread_id,
        "approved"
    )
    else:
        status = "ended"
        update_ticket_status(request.thread_id, "rejected")

    return {
        "status": status,
        "data": final_state.values
    }