from utils.helpers import execute_query, fetch_all, fetch_one


def get_expenditures():
    return fetch_all("SELECT * FROM expenditures ORDER BY created_at DESC")


def get_expenditure_totals():
    return fetch_one(
        "SELECT COALESCE(SUM(amount), 0) AS total_spent, COUNT(*) AS total_records FROM expenditures"
    )


def insert_expenditure(event_name, amount, purpose, created_at):
    execute_query(
        """
        INSERT INTO expenditures (event_name, amount, purpose, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (event_name, amount, purpose, created_at),
    )


def update_expenditure(expenditure_id, event_name, amount, purpose, created_at):
    execute_query(
        """
        UPDATE expenditures
        SET event_name = ?, amount = ?, purpose = ?, created_at = ?
        WHERE id = ?
        """,
        (event_name, amount, purpose, created_at, expenditure_id),
    )


def delete_expenditure(expenditure_id):
    execute_query("DELETE FROM expenditures WHERE id = ?", (expenditure_id,))
