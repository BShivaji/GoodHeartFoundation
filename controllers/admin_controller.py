from collections import Counter, defaultdict
from datetime import datetime

from models.admin_model import get_admin_by_username
from models.event_model import get_events
from models.fund_model import get_fund_totals, get_funds
from models.volunteer_model import get_volunteers
from utils.auth import verify_password


def check_admin_login(username, password):
    admin = get_admin_by_username(username)
    if not admin:
        return False
    return verify_password(password, admin["password"])


def build_dashboard_stats():
    volunteers = get_volunteers()
    events = get_events()
    donors = get_funds()
    funds = get_fund_totals() or {"total_raised": 0, "total_donors": 0}

    growth_labels = _last_six_month_labels()
    volunteer_growth = _count_by_month(volunteers, growth_labels)
    event_growth = _count_by_month(events, growth_labels)
    donor_growth = _count_by_month(donors, growth_labels)

    area_counter = Counter(
        volunteer.get("area_interest") or "General Support"
        for volunteer in volunteers
    )
    area_breakdown = [
        {"label": label, "value": value}
        for label, value in area_counter.most_common(5)
    ]

    purpose_totals = defaultdict(float)
    for donor in donors:
        purpose_totals[donor.get("purpose") or "General Donation"] += float(donor.get("amount", 0))
    purpose_breakdown = [
        {"label": label, "value": round(value, 2)}
        for label, value in sorted(purpose_totals.items(), key=lambda item: item[1], reverse=True)[:5]
    ]

    impact_total = max(
        1,
        len(volunteers) + len(events) + int(funds.get("total_donors", 0)),
    )
    impact_segments = [
        {"label": "Volunteers", "value": len(volunteers), "color": "#c46a2f"},
        {"label": "Events", "value": len(events), "color": "#355242"},
        {"label": "Donors", "value": int(funds.get("total_donors", 0)), "color": "#8f4b1f"},
    ]
    pie_gradient = _build_conic_gradient(impact_segments, impact_total)

    return {
        "volunteers": len(volunteers),
        "events": len(events),
        "funds": funds["total_raised"],
        "total_donors": int(funds.get("total_donors", 0)),
        "growth_labels": growth_labels,
        "volunteer_growth": volunteer_growth,
        "event_growth": event_growth,
        "donor_growth": donor_growth,
        "growth_max": max(1, *(volunteer_growth + event_growth + donor_growth)),
        "area_breakdown": area_breakdown,
        "area_breakdown_max": max(1, *[item["value"] for item in area_breakdown]) if area_breakdown else 1,
        "purpose_breakdown": purpose_breakdown,
        "purpose_breakdown_max": max(1, *[item["value"] for item in purpose_breakdown]) if purpose_breakdown else 1,
        "impact_segments": impact_segments,
        "impact_gradient": pie_gradient,
    }


def _last_six_month_labels():
    now = datetime.now()
    labels = []
    month = now.month
    year = now.year
    for _ in range(5, -1, -1):
        calc_month = month - _
        calc_year = year
        while calc_month <= 0:
            calc_month += 12
            calc_year -= 1
        labels.append(f"{calc_year:04d}-{calc_month:02d}")
    return labels


def _count_by_month(records, labels):
    counts = {label: 0 for label in labels}
    for record in records:
        created_at = record.get("created_at", "")
        if len(created_at) >= 7:
            label = created_at[:7]
            if label in counts:
                counts[label] += 1
    return [counts[label] for label in labels]


def _build_conic_gradient(segments, total):
    start = 0
    gradient_parts = []
    for segment in segments:
        portion = (segment["value"] / total) * 100 if total else 0
        end = start + portion
        gradient_parts.append(f"{segment['color']} {start:.2f}% {end:.2f}%")
        start = end
    return "conic-gradient(" + ", ".join(gradient_parts) + ")"
