from utils.helpers import execute_query, fetch_all, fetch_one


def get_funds():
    return fetch_all("SELECT * FROM funds ORDER BY created_at DESC")


def insert_fund(donor_name, amount, purpose, created_at):
    execute_query(
        """
        INSERT INTO funds (donor_name, amount, purpose, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (donor_name, amount, purpose, created_at),
    )


def update_fund(fund_id, donor_name, amount, purpose, created_at):
    execute_query(
        """
        UPDATE funds
        SET donor_name = ?, amount = ?, purpose = ?, created_at = ?
        WHERE id = ?
        """,
        (donor_name, amount, purpose, created_at, fund_id),
    )


def delete_fund(fund_id):
    execute_query("DELETE FROM funds WHERE id = ?", (fund_id,))


def get_fund_totals():
    return fetch_one(
        "SELECT COALESCE(SUM(amount), 0) AS total_raised, COUNT(*) AS total_donors FROM funds"
    )
