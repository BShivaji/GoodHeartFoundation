from models.fund_model import delete_fund, get_fund_totals, get_funds, insert_fund, update_fund
from utils.validators import validate_required_fields


def create_fund(form_data):
    validate_required_fields(form_data, ["donor_name", "donation_date", "amount", "purpose"])
    insert_fund(
        form_data.get("donor_name", "").strip(),
        float(form_data.get("amount", 0)),
        form_data.get("purpose", "").strip(),
        f"{form_data.get('donation_date', '').strip()} 10:00:00",
    )


def edit_fund(fund_id, form_data):
    validate_required_fields(form_data, ["donor_name", "donation_date", "amount", "purpose"])
    update_fund(
        fund_id,
        form_data.get("donor_name", "").strip(),
        float(form_data.get("amount", 0)),
        form_data.get("purpose", "").strip(),
        f"{form_data.get('donation_date', '').strip()} 10:00:00",
    )


def remove_fund(fund_id):
    delete_fund(fund_id)


def get_fund_summary():
    summary = get_fund_totals()
    summary = summary or {"total_raised": 0, "total_donors": 0}
    summary["donors"] = get_funds()
    return summary
