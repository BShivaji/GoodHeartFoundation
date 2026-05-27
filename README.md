# Good Heart Foundation

A starter Flask project scaffold for an NGO website with user pages, volunteer management, events, gallery, and a simple admin area.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## Project areas

- `routes/` contains Flask blueprints.
- `controllers/` keeps request-facing business logic.
- `models/` contains SQLite data access helpers.
- `templates/` stores Jinja templates.
- `static/` contains CSS, JavaScript, images, and uploads.
- `database/schema.sql` defines the SQLite schema used to bootstrap `database/ngo.db`.
