from utils.helpers import execute_query, fetch_all


def insert_event(title, description, event_date, location):
    execute_query(
        """
        INSERT INTO events (title, description, event_date, location)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, event_date, location),
    )


def get_events():
    return fetch_all("SELECT * FROM events ORDER BY event_date ASC")


def update_event_date(event_id, event_date):
    execute_query(
        """
        UPDATE events
        SET event_date = ?
        WHERE id = ?
        """,
        (event_date, event_id),
    )


def delete_event(event_id):
    execute_query("DELETE FROM events WHERE id = ?", (event_id,))
