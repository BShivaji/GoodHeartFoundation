from utils.helpers import execute_query, fetch_all


def get_recent_works():
    return fetch_all("SELECT * FROM recent_works ORDER BY created_at DESC")


def insert_recent_work(title, description, image_path):
    execute_query(
        """
        INSERT INTO recent_works (title, description, image_path)
        VALUES (?, ?, ?)
        """,
        (title, description, image_path),
    )


def delete_recent_work(work_id):
    execute_query("DELETE FROM recent_works WHERE id = ?", (work_id,))
