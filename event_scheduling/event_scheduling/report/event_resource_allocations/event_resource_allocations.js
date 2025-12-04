// Copyright (c) 2025, Praveen and contributors
// For license information, please see license.txt

frappe.query_reports["Event Resource Allocations"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": (" From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": (" To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "event",
			"label": ("Event"),
			"fieldtype": "Link",
			"options": "Events"
		},
		{
			"fieldname": "resource_type",
			"label": ("Resource Type"),
			"fieldtype": "Link",
			"options": "Resource Type",
		},
		{
			"fieldname": "resource_name",
			"label": ("Resource Name"),
			"fieldtype": "Link",
			"options": "Resources"
		},
	]
};
