# Copyright (c) 2025, Praveen and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_datetime, getdate, now_datetime

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Resource Name", "fieldname": "resource_name", "fieldtype": "Link", "options": "Resources", "width": 200},
        {"label": "Resource Type", "fieldname": "resource_type", "fieldtype": "Data", "width": 150},
        {"label": "Total Events", "fieldname": "total_events", "fieldtype": "Int", "width": 120},
        {"label": "Total Utilized Hours", "fieldname": "total_hours", "fieldtype": "Float", "width": 200},
        {"label": "Upcoming Events", "fieldname": "upcoming", "fieldtype": "Int", "width": 150},
        {"label": "Utilised Events", "fieldname": "utilised", "fieldtype": "Int", "width": 150},
    ]

def get_data(filters):
    today = now_datetime()

    summary = {}

    parent_filters = {}
    if filters.get("event"):
        parent_filters["events"] = filters.get("event")

    parent_docs = frappe.get_all(
        "Event Resource Allocation",
        filters=parent_filters,
        fields=["name", "events"]
    )

    for parent in parent_docs:

        event_doc = frappe.get_doc("Events", parent.events)

        if filters.get("from_date") and event_doc.start_time.date() < getdate(filters.get("from_date")):
            continue
        if filters.get("to_date") and event_doc.end_time.date() > getdate(filters.get("to_date")):
            continue

        alloc_doc = frappe.get_doc("Event Resource Allocation", parent.name)

        for row in alloc_doc.allocations:

            if filters.get("resource_type") and row.resource_type != filters.get("resource_type"):
                continue
            if filters.get("resource_name") and row.resource_name != filters.get("resource_name"):
                continue

            start = get_datetime(event_doc.start_time)
            end = get_datetime(event_doc.end_time)
            hours_used = (end - start).total_seconds() / 3600

            status = "Upcoming" if start > today else "Utilised"

            key = row.resource_name

            if key not in summary:
                summary[key] = {
                    "resource_name": row.resource_name,
                    "resource_type": row.resource_type,
                    "total_hours": 0,
                    "total_events": 0,
                    "upcoming": 0,
                    "utilised": 0
                }

            summary[key]["total_hours"] += hours_used
            summary[key]["total_events"] += 1

            if status == "Upcoming":
                summary[key]["upcoming"] += 1
            else:
                summary[key]["utilised"] += 1

    final = []
    for key, s in summary.items():
        final.append({
            "resource_name": s["resource_name"],
            "resource_type": s["resource_type"],
            "total_events": s["total_events"],
            "total_hours": round(s["total_hours"], 2),
            "upcoming": s["upcoming"],
            "utilised": s["utilised"]
        })

    return final
