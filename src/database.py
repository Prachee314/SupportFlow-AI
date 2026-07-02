import sqlite3
from datetime import datetime


def setup_customers_db():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT,
            tier TEXT,
            balance REAL,
            status TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM customers")

    if cursor.fetchone()[0] == 0:
        customers = [
            ("CUST-101", "Alice Smith", "Enterprise", -250.0, "Active"),
            ("CUST-102", "Bob Jones", "Standard", 0.0, "Active"),
            ("CUST-103", "Charlie Brown", "Free", -15.5, "Suspended")
        ]

        cursor.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
            customers
        )

    conn.commit()
    conn.close()


def setup_tickets_db():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_id TEXT,
            issue_type TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tickets")

    if cursor.fetchone()[0] == 0:
        tickets = [
    (
        "TKT-001",
        "CUST-101",
        "billing",
        "High",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    (
        "TKT-002",
        "CUST-102",
        "technical",
        "Medium",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    (
        "TKT-003",
        "CUST-101",
        "refund",
        "High",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    (
        "TKT-004",
        "CUST-102",
        "account",
        "Medium",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    (
        "TKT-005",
        "CUST-103",
        "security",
        "Critical",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ),
    (
        "TKT-006",
        "CUST-101",
        "technical",
        "Critical",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
]

        cursor.executemany(
            "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)",
            tickets
        )

    conn.commit()
    conn.close()


def initialize_database():
    setup_customers_db()
    setup_tickets_db()
    print("Database ready")


if __name__ == "__main__":
    initialize_database()