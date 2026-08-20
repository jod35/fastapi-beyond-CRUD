import os
from datetime import datetime
import sqlite3
from typing import Any

DB_PATH = os.environ.get("MICROFINANCE_DB", "microfinance.sqlite3")

UPDATEABLE_COLUMNS = {
    "first_name",
    "surname",
    "date_of_birth",
    "gender",
    "email",
    "national_id",
    "phone_number",
}


def get_connection() -> sqlite3.Connection:
    """provide a connection to the db"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database by creating table"""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER ,
                first_name VARCHAR(25),
                surname VARCHAR(25),
                date_of_birth DATE,
                gender VARCHAR(10),
                email VARCHAR(30) UNIQUE,
                national_id VARCHAR(14) UNIQUE,
                phone_number VARCHAR(10) UNIQUE,
                status VARCHAR(10) DEFAULT 'inactive',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id)
            );
            """)

        conn.commit()
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row) -> dict[Any, Any]:
    return dict(row)


def create_customer(data: dict) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO customers (first_name,surname,date_of_birth,gender,email,national_id,phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                data["first_name"],
                data["surname"],
                data["date_of_birth"],
                data["gender"],
                data.get("email"),
                data["national_id"],
                data["phone_number"],
            ),
        )

        conn.commit()
        return cursor.lastrowid # type: ignore
    finally:
        conn.close()


def list_all_customers() -> list[dict[Any, Any]]:
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT * FROM customers;")
        return [row_to_dict(r) for r in cursor.fetchall() if r is not None]
    finally:
        conn.close()


def get_customer_by_id(customer_id: int) -> dict[Any, Any] | None:
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT * FROM customers WHERE id = ?;", (customer_id,))
        result = cursor.fetchone()
        return row_to_dict(result) if result is not None else None
    finally:
        conn.close()


def update_customer(customer_id: int, data: dict) -> dict | None:
    """Update a customer's information."""
    fields = {
        key: value
        for key, value in data.items()
        if key in UPDATEABLE_COLUMNS and value is not None
    }
    if not fields:
        return get_customer_by_id(customer_id)
    fields["updated_at"] = datetime.now().isoformat()
    set_clause = ", ".join(f"{key} = ?" for key in fields)
    values_tuple = tuple(fields.values()) + (customer_id,)
    conn = get_connection()
    try:
        conn.execute(f"UPDATE customers SET {set_clause} WHERE id = ?", values_tuple)
        conn.commit()
        return get_customer_by_id(customer_id)
    finally:
        conn.close()


def delete_customer(customer_id: int) -> bool:
    """Delete a customer."""

    conn = get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM customers WHERE id = ?",
            (customer_id,),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
