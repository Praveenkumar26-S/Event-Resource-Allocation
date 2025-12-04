# Copyright (c) 2025, Praveen and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document
from frappe.utils import get_datetime

class AllocationTool(Document):
	pass


@frappe.whitelist()
def confirm_allocation(event, allocations):

    if isinstance(allocations, str):
        allocations = json.loads(allocations)

    event_doc = frappe.get_doc("Events", event)
    event_start = get_datetime(event_doc.start_time)
    event_end = get_datetime(event_doc.end_time)

    valid_rows = []
    conflicts = []

    existing_allocs = frappe.get_all(
        "Event Resource Allocation",
        fields=["name", "events", "resource_name", "resource_type"]
    )

    for row in allocations:
        resource_name = row.get("resource_name")
        resource_type = row.get("resource_type")

        is_conflict = False

        for alloc in existing_allocs:

            if alloc.resource_name == resource_name:

                other_event = frappe.get_doc("Events", alloc.events)
                other_start = get_datetime(other_event.start_time)
                other_end = get_datetime(other_event.end_time)

                if event_start < other_end and event_end > other_start:
                    conflicts.append(
                        f"{resource_name} ({resource_type}) already allocated for Event {other_event.name},({other_event.start_time} to {other_event.end_time}),({alloc.name})"
                    )
                    is_conflict = True
                    break

        if not is_conflict:
            valid_rows.append(row)

    if not valid_rows:
        return {
            "success": None,
            "conflicts": conflicts
        }

    created = []
    print("Valid Rows:", valid_rows)
    for row in valid_rows:
        new_doc = frappe.new_doc("Event Resource Allocation")
        new_doc.events = event
        new_doc.resource_type = row.get("resource_type")
        new_doc.resource_name = row.get("resource_name")
        new_doc.insert()
        created.append(new_doc.name)

    return {
        "success": created,
        "conflicts": conflicts
    }
