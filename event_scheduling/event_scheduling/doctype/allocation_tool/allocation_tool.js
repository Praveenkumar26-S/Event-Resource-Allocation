// Copyright (c) 2025, Praveen and contributors
// For license information, please see license.txt


frappe.ui.form.on("Allocation Tool", {
    refresh(frm) {
        frm.disable_save();
        
        frm.set_value("allocations", []);
        frm.set_value("events", "");
        
        frm.set_query("events", function() {
            return{
                filters: {
                    status: "Active"
                }
            };
        });

        frm.fields_dict["allocations"].grid.get_field("resource_name").get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                filters: {
                    resource_type: child.resource_type,
                    status: "Active"
                }
            };
        }

        frm.add_custom_button("Confirm Allocation", function () {

            frappe.call({
                method: "event_scheduling.event_scheduling.doctype.allocation_tool.allocation_tool.confirm_allocation",
                args: {
                    event: frm.doc.events,
                    allocations: JSON.stringify(frm.doc.allocations)
                },
                callback: function(r) {
                    if (!r.message) return;

                    let msg = r.message;

                    if (!msg.success) {
                        frappe.msgprint({
                            title: __("Allocation Conflicts"),
                            indicator: "red",
                            message: msg.conflicts.join("<br>")
                        });

                    }

                    if (msg.success) {
                        frappe.msgprint(`
                            <b>Allocation Created:</b> ${msg.success}<br>
                            <br>
                            <b>Conflicts:</b><br>
                            ${msg.conflicts.join("<br>")}
                        `);
                        frm.reload_doc();
                    }
                }
            });
        });

        frm.add_custom_button("Go to Event Resource Allocation List", function(){
            frappe.set_route("List", "Event Resource Allocation");
        });
    }
});
