from utils.helpers import execute_query, fetch_all


def insert_volunteer(name, email, gender, place, phone, message, area_interest, document_path):
    execute_query(
        """
        INSERT INTO volunteers (name, email, gender, place, phone, message, area_interest, document_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (name, email, gender, place, phone, message, area_interest, document_path),
    )


def get_volunteers():
    return fetch_all("SELECT * FROM volunteers ORDER BY created_at DESC")
