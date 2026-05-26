from models.expenditure_model import (
    delete_expenditure,
    get_expenditures,
    get_expenditure_totals,
    insert_expenditure,
    update_expenditure,
)
from utils.validators import validate_required_fields


def get_expenditure_summary():
    summary = get_expenditure_totals() or {"total_spent": 0, "total_records": 0}
    summary["records"] = get_expenditures()
    return summary


def create_expenditure(form_data):
    validate_required_fields(form_data, ["event_name", "expense_date", "amount", "purpose"])
    insert_expenditure(
        form_data.get("event_name", "").strip(),
        float(form_data.get("amount", 0)),
        form_data.get("purpose", "").strip(),
        f"{form_data.get('expense_date', '').strip()} 12:00:00",
    )


def edit_expenditure(expenditure_id, form_data):
    validate_required_fields(form_data, ["event_name", "expense_date", "amount", "purpose"])
    update_expenditure(
        expenditure_id,
        form_data.get("event_name", "").strip(),
        float(form_data.get("amount", 0)),
        form_data.get("purpose", "").strip(),
        f"{form_data.get('expense_date', '').strip()} 12:00:00",
    )


def remove_expenditure(expenditure_id):
    delete_expenditure(expenditure_id)
