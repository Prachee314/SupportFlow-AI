import re

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

from src.state import SupportState
from src.tools import fetch_customer, fetch_ticket

load_dotenv()


# ---------- TRIAGE ----------

class TriageOutput(BaseModel):
    category: str = Field(
        description="billing, technical or general"
    )


def triage_node(state: SupportState):
    # Unchanged: classifies based on the latest message only. Re-running
    # triage on every new message from the same customer is intentional —
    # a follow-up query can be a completely different issue type than
    # their first one (e.g. first message is billing, second is
    # technical), so the category should reflect what they're asking
    # about NOW, not be frozen from their very first message.
    llm = ChatGroq(
        model="llama-3.3-70b-versatile"
    ).with_structured_output(TriageOutput)

    prompt = f"""
    Classify this customer query into exactly one category:

    billing
    technical
    general

    Query:
    {state["customer_query"]}
    """

    result = llm.invoke(prompt)

    return {
        "category": result.category
    }


# ---------- PRIORITY ----------

class PriorityOutput(BaseModel):
    priority: str = Field(
        description="Low, Medium, High or Critical"
    )


def priority_node(state: SupportState):
    # Unchanged for the same reason as triage_node — priority should
    # reflect the urgency of what they're asking right now.
    llm = ChatGroq(
        model="llama-3.3-70b-versatile"
    ).with_structured_output(PriorityOutput)

    prompt = f"""
    Assign ticket priority.

    Low:
    General questions

    Medium:
    Refund requests

    High:
    Billing failures

    Critical:
    Hacked account, security breach,
    complete service outage

    Query:
    {state["customer_query"]}
    """

    result = llm.invoke(prompt)

    return {
        "priority": result.priority
    }


# ---------- DATABASE ----------

def database_node(state: SupportState):
    # Unchanged — still looks for a CUST-/TKT- ID in the latest message.
    # If an earlier message in the history mentioned an ID but the
    # latest one doesn't repeat it, this node won't find it again; that
    # is a known limitation worth flagging rather than silently fixing
    # here, since broadening the regex search to the full history is a
    # separate, larger change (deciding which historical ID should "win"
    # if multiple different IDs were ever mentioned).
    query = state["customer_query"]

    customer_match = re.search(
        r"CUST-\d+",
        query,
        re.IGNORECASE
    )

    ticket_match = re.search(
        r"TKT-\d+",
        query,
        re.IGNORECASE
    )

    customer = None
    ticket = None

    if customer_match:
        customer = fetch_customer(
            customer_match.group().upper()
        )

    if ticket_match:
        ticket = fetch_ticket(
            ticket_match.group().upper()
        )

    return {
        "customer_id":
            customer_match.group().upper()
            if customer_match else None,

        "ticket_id":
            ticket_match.group().upper()
            if ticket_match else None,

        "customer_details": customer,
        "ticket_details": ticket
    }


# ---------- RESOLUTION ----------

def resolution_node(state: SupportState):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.4
    )

    feedback = state.get("supervisor_feedback")
    previous_draft = state.get("draft_response")

    # NEW: build a readable transcript of every message this customer
    # has sent on this ticket so far, oldest first. Without this, a
    # customer's second or third message would be drafted as if it were
    # their very first contact — the agent would have no idea they'd
    # already asked something earlier in the same ticket.
    history = state.get("query_history", [])
    if history:
        conversation = "\n".join(
            f"[{entry['submitted_at']}] {entry['text']}"
            for entry in history
        )
    else:
        # Defensive fallback for tickets created before query_history
        # existed, or if it's ever empty for any reason.
        conversation = state["customer_query"]

    if feedback:
        prompt = f"""
        You are a professional customer support agent.

        A supervisor REJECTED your previous draft response and gave
        feedback. Your job now is to REVISE the previous draft to
        directly address that feedback — do not just restate the
        original draft, and do not ignore the feedback.

        Full conversation with this customer so far (oldest first):
        {conversation}

        Most recent message (what you are currently responding to):
        {state["customer_query"]}

        Category:
        {state["category"]}

        Priority:
        {state["priority"]}

        Customer Details:
        {state["customer_details"]}

        Ticket Details:
        {state["ticket_details"]}

        Previous Draft Response:
        {previous_draft}

        Supervisor Feedback (you MUST address this):
        {feedback}

        Write a new, revised response that fixes what the supervisor
        flagged. Keep it professional. Do not mention the supervisor,
        the review process, or that this is a revision — write it as a
        normal customer-facing response.
        """
    else:
        prompt = f"""
        You are a professional customer support agent.

        Full conversation with this customer so far (oldest first):
        {conversation}

        Most recent message (what you are currently responding to):
        {state["customer_query"]}

        Category:
        {state["category"]}

        Priority:
        {state["priority"]}

        Customer Details:
        {state["customer_details"]}

        Ticket Details:
        {state["ticket_details"]}

        Draft a helpful and professional response. If the customer has
        contacted us before on this ticket, acknowledge the context
        naturally rather than treating this as their first message.
        """
    
    print("=" * 80)
    print("RESOLUTION NODE CALLED")
    print("Supervisor Feedback:", feedback)
    print("Previous Draft:", previous_draft)
    print("=" * 80)

    response = llm.invoke(prompt)
    print("NEW DRAFT GENERATED:")
    print(response.content)
    print("=" * 80)
    return {
        "draft_response": response.content
    }


# ---------- FINAL ACTION ----------

def execute_action_node(state: SupportState):
    return {
        "final_action": "Response sent successfully"
    }