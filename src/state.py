from typing import TypedDict, Optional, List


class QueryEntry(TypedDict):
    text: str
    submitted_at: str  # "%Y-%m-%d %H:%M:%S"

class ConversationEntry(TypedDict):
    role: str
    text: str
    submitted_at: str

class SupportState(TypedDict):
    # Always holds the LATEST message the customer sent. Kept as a plain
    # string (not a list) so triage_node, priority_node, database_node,
    # and resolution_node — which all read this directly for prompts and
    # regex matching — continue to work without changes.
    customer_query: str

    # NEW: the full running history of every message this customer has
    # sent on this one ticket, oldest first. This is what makes "one
    # ticket per customer, every query visible to the supervisor"
    # possible — customer_query alone only ever shows the newest message.
    query_history: List[QueryEntry]

    category: Optional[str]
    conversation_history: List[ConversationEntry]
    priority: Optional[str]

    customer_id: Optional[str]
    ticket_id: Optional[str]

    customer_details: Optional[dict]
    ticket_details: Optional[dict]

    draft_response: Optional[str]

    supervisor_approved: Optional[bool]
    supervisor_feedback: Optional[str]

    final_action: Optional[str]