import sqlite3


def fetch_customer(customer_id):
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE customer_id = ?",
        (customer_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def fetch_ticket(ticket_id):
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE ticket_id = ?",
        (ticket_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def create_ticket(ticket_id, customer_id, issue_type, priority):
    conn = sqlite3.connect("tickets.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            ticket_id,
            customer_id,
            issue_type,
            priority,
            "Open"
        )
    )

    conn.commit()
    conn.close()


def update_ticket_status(ticket_id, new_status):
    conn = sqlite3.connect("tickets.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (new_status, ticket_id)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(fetch_customer("CUST-101"))
    print(fetch_ticket("TKT-001"))