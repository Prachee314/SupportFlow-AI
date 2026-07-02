"""
Live Ticket Queue

This database stores all customer submitted tickets that are waiting for
supervisor review.

LangGraph still uses `thread_id` internally.

Customers only see a formatted Support Ticket ID like

TKT-8A91F3D2

Both values point to the same thread.
"""

import sqlite3
import uuid
from datetime import datetime
from typing import Optional

DB_PATH = "queue.db"


# ------------------------------------------------------
# Database
# ------------------------------------------------------

def setup_queue_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_queue(

        thread_id TEXT PRIMARY KEY,

        customer_name TEXT,

        customer_email TEXT,

        status TEXT NOT NULL,

        created_at TEXT NOT NULL,

        updated_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------
# Ticket Helpers
# ------------------------------------------------------

def generate_thread_id():

    """
    Internal LangGraph thread id.

    Customer never sees this directly.
    """

    return uuid.uuid4().hex[:8].upper()


def format_ticket_id(thread_id: str):

    """
    Customer-facing ticket id.
    """

    return f"TKT-{thread_id}"


# ------------------------------------------------------
# Create Ticket
# ------------------------------------------------------

def enqueue_ticket(
    thread_id: str,
    customer_name: str,
    customer_email: str
):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ticket_queue(

            thread_id,
            customer_name,
            customer_email,
            status,
            created_at,
            updated_at

        )

        VALUES(?,?,?,?,?,?)

        ON CONFLICT(thread_id)

        DO UPDATE SET

            customer_name=excluded.customer_name,

            customer_email=excluded.customer_email,

            status='pending_review',

            updated_at=excluded.updated_at
        """,
        (
            thread_id,
            customer_name,
            customer_email,
            "pending_review",
            now,
            now
        )
    )

    conn.commit()
    conn.close()


# ------------------------------------------------------
# Update Status
# ------------------------------------------------------

def update_ticket_status(
    thread_id: str,
    status: str
):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ticket_queue

        SET

            status=?,
            updated_at=?

        WHERE thread_id=?
        """,
        (
            status,
            now,
            thread_id
        )
    )

    conn.commit()
    conn.close()


# ------------------------------------------------------
# Queue
# ------------------------------------------------------

def get_next_pending_ticket():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT thread_id

        FROM ticket_queue

        WHERE status='pending_review'

        ORDER BY created_at ASC

        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None


# ------------------------------------------------------
# Ticket Info
# ------------------------------------------------------

def get_ticket_info(thread_id):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM ticket_queue

        WHERE thread_id=?
        """,
        (thread_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        data = dict(row)

        data["ticket_id"] = format_ticket_id(thread_id)

        return data

    return None


# ------------------------------------------------------
# Queue Counts
# ------------------------------------------------------

def get_queue_counts():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status,COUNT(*)

        FROM ticket_queue

        GROUP BY status
        """
    )

    rows = cursor.fetchall()

    conn.close()

    counts = {

        "pending_review": 0,

        "approved": 0,

        "rejected": 0

    }

    counts.update({

        status: count

        for status, count in rows

    })

    return counts


# ------------------------------------------------------
# Ticket Exists
# ------------------------------------------------------

def ticket_exists(thread_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1

        FROM ticket_queue

        WHERE thread_id=?
        """,
        (thread_id,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


# ------------------------------------------------------
# Testing
# ------------------------------------------------------

if __name__ == "__main__":

    setup_queue_db()

    print("Queue Ready")

    tid = generate_thread_id()

    enqueue_ticket(
        tid,
        "Alice",
        "alice@gmail.com"
    )

    print(get_ticket_info(tid))

    print(get_queue_counts())