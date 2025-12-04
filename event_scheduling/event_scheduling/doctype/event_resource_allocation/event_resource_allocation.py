# Copyright (c) 2025, Praveen and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document
from frappe.utils import get_datetime

class EventResourceAllocation(Document):

    def validate(self):
        self.check_conflicts()

    def check_conflicts(self):
        event = frappe.get_doc("Events", self.events)
        start = get_datetime(event.start_time)
        end = get_datetime(event.end_time)

        other_docs = frappe.get_all(
            "Event Resource Allocation",
            filters={"name": ("!=", self.name)},
            fields=["name", "events", "resource_name"]
        )

        for doc in other_docs:
            if doc.resource_name == self.resource_name:
                other_event = frappe.get_doc("Events", doc.events)
                other_start = get_datetime(other_event.start_time)
                other_end = get_datetime(other_event.end_time)

                if start < other_end and end > other_start:
                    frappe.throw(
                        f"The resource {self.resource_name} ({self.resource_type}) is already allocated to event {other_event.name} during this time."
                    )
