import os
import sqlite3


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_db_connection(database_path=None):
    db_path = database_path or os.path.join(BASE_DIR, "database", "ngo.db")
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def execute_query(query, params=()):
    connection = get_db_connection()
    try:
        connection.execute(query, params)
        connection.commit()
    finally:
        connection.close()


def fetch_all(query, params=()):
    connection = get_db_connection()
    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def fetch_one(query, params=()):
    connection = get_db_connection()
    try:
        row = connection.execute(query, params).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def ensure_database(database_path):
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    if os.path.exists(database_path) and os.path.getsize(database_path) > 0:
        _ensure_volunteer_columns(database_path)
        _ensure_fund_columns(database_path)
        _ensure_expenditure_table(database_path)
        _ensure_recent_works_table(database_path)
        return

    schema_path = os.path.join(BASE_DIR, "database", "schema.sql")
    connection = sqlite3.connect(database_path)
    try:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            connection.executescript(schema_file.read())
        connection.commit()
    finally:
        connection.close()

    _ensure_volunteer_columns(database_path)
    _ensure_fund_columns(database_path)
    _ensure_expenditure_table(database_path)
    _ensure_recent_works_table(database_path)


def _ensure_volunteer_columns(database_path):
    connection = sqlite3.connect(database_path)
    try:
        existing_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(volunteers)").fetchall()
        }
        for column_name, column_sql in (
            ("gender", "ALTER TABLE volunteers ADD COLUMN gender TEXT"),
            ("place", "ALTER TABLE volunteers ADD COLUMN place TEXT"),
            ("area_interest", "ALTER TABLE volunteers ADD COLUMN area_interest TEXT"),
        ):
            if column_name not in existing_columns:
                connection.execute(column_sql)
        connection.commit()
    finally:
        connection.close()


def _ensure_fund_columns(database_path):
    connection = sqlite3.connect(database_path)
    try:
        existing_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(funds)").fetchall()
        }
        if "purpose" not in existing_columns:
            connection.execute("ALTER TABLE funds ADD COLUMN purpose TEXT")
            purpose_updates = [
                ("Medical Awareness Camp", 1),
                ("Plantation for Nature", 2),
                ("Social Welfare Kits", 3),
                ("Education Support Program", 4),
                ("Animal Welfare Feeding Drive", 5),
                ("Fund Raising Event Support", 6),
                ("Medical Awareness Camp", 7),
                ("Tree Plantation Activity", 8),
                ("Community Relief Materials", 9),
                ("Social Welfare Outreach", 10),
                ("Volunteer Orientation Support", 11),
                ("Clothing and Essentials Distribution", 12),
                ("Education Materials", 13),
                ("Nature Protection Initiative", 14),
                ("Animal Welfare Support", 15),
            ]
            connection.executemany(
                "UPDATE funds SET purpose = ? WHERE id = ?",
                purpose_updates,
            )
        connection.commit()
    finally:
        connection.close()


def _ensure_expenditure_table(database_path):
    connection = sqlite3.connect(database_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenditures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                amount REAL NOT NULL,
                purpose TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        existing_count = connection.execute("SELECT COUNT(*) FROM expenditures").fetchone()[0]
        if existing_count == 0:
            seed_rows = [
                ("Community Breakfast Drive", 4200.00, "Food packets and logistics", "2026-04-01 12:00:00"),
                ("School Supply Donation Camp", 5600.00, "School kits and transport", "2026-04-02 12:00:00"),
                ("Women Wellness Workshop", 6800.00, "Awareness materials and setup", "2026-04-03 12:00:00"),
                ("Medical Checkup Camp", 12500.00, "Medical supplies and registrations", "2026-04-04 12:00:00"),
                ("Youth Career Guidance Session", 3500.00, "Printed materials and refreshments", "2026-04-05 12:00:00"),
                ("Clothes Distribution Day", 7100.00, "Packaging and local transport", "2026-04-06 12:00:00"),
                ("Senior Citizen Care Visit", 2900.00, "Care packs and volunteer travel", "2026-04-07 12:00:00"),
                ("Nutrition Awareness Program", 4800.00, "Educational kits and venue support", "2026-04-08 12:00:00"),
                ("Blood Donation Camp", 8400.00, "Medical assistance and banners", "2026-04-09 12:00:00"),
                ("Evening Study Circle", 2600.00, "Study materials and snacks", "2026-04-10 12:00:00"),
                ("Monsoon Relief Preparation", 9300.00, "Emergency kit preparation", "2026-04-11 12:00:00"),
                ("Community Clean-Up Drive", 3900.00, "Gloves, bags, and signage", "2026-04-12 12:00:00"),
                ("Parents Counseling Meet", 3100.00, "Session setup and stationery", "2026-04-13 12:00:00"),
                ("Fundraising Dinner", 15200.00, "Venue and hospitality", "2026-04-14 12:00:00"),
                ("Volunteer Orientation Day", 4400.00, "Welcome kits and presentation setup", "2026-04-15 12:00:00"),
            ]
            connection.executemany(
                """
                INSERT INTO expenditures (event_name, amount, purpose, created_at)
                VALUES (?, ?, ?, ?)
                """,
                seed_rows,
            )
        connection.commit()
    finally:
        connection.close()


def _ensure_recent_works_table(database_path):
    connection = sqlite3.connect(database_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS recent_works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()
