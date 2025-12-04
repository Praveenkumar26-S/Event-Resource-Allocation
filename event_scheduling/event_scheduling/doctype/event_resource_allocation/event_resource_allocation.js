// Copyright (c) 2025, Praveen and contributors
// For license information, please see license.txt


frappe.ui.form.on("Event Resource Allocation", {
    refresh(frm) {
        frm.set_query("events", function() {
            return {
                filters: {
                    status: "Active"
                }
            };
        });
        frm.set_query("resource_name", function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                filters: {
                    resource_type: child.resource_type,
                    status: "Active"
                }
            };
        });
    }
});