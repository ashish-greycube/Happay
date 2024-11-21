// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project Travel Request", {
    setup(frm) {
        frm.set_query("cost_center", function (doc) {
            return {
                filters: {
                    "company": doc.company,
                    "is_group": 0
                },
            }
        })
        frm.set_query("expense_account", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "root_type":"Expense",
                    "is_group":0
                },
            }
        })        
        frm.set_query("travel_agent", function(doc){
            return {
                filters: {
                    "company": doc.company
                },
            }
        })
        frm.set_query("department", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "is_group":0
                },
            }
        })
    },

    refresh(frm){
        if (frm.doc.workflow_state == "Approved" && frm.doc.docstatus == 1 && frm.doc.docstatus && frm.doc.service_charge) {
            frm.add_custom_button(__('Vendor Invoice'), () => create_vendor_invoice_from_project_travel_request(frm), __("Create"));
        }
    },

    booking_for(frm) {
        if (frm.doc.booking_for == "Self") {
            frappe.call({
                method: "happay.happay.doctype.project_travel_request.project_travel_request.get_employee_detail",
                args: {
                    "session_user": frappe.session.user
                },
                callback: function (response) {
                    let employee_detail = response.message
                    if (employee_detail) {
                        frm.set_value("passenger_first_name", employee_detail.first_name)
                        frm.set_value("passenger_last_name", employee_detail.last_name)
                        frm.set_value("passenger_gender", employee_detail.gender)
                    }
                }
            })
        }
    },

    company(frm){
        frappe.db.get_value("Company",{"name":frm.doc.company},["custom_travel_expense_account"])
        .then(r => {
            console.log(r)
            let expense_account = r.message.custom_travel_expense_account
            frm.set_value("expense_account", expense_account)
        })
    },

    cost_center(frm) {
        let cost_center = frm.doc.cost_center
        frm.set_value("project_manager", "")
        frm.set_value("project_manager_name", "")
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_pm_and_account_from_cost_center",
            args: {
                "cost_center": cost_center
            },
            callback: function (response) {
                let cc_detials = response.message
                if (cc_detials) {
                    frm.set_value("project_manager", cc_detials.custom_project_manager)
                    frm.set_value("project_manager_name", cc_detials.project_manager_name)
                }
            }
        })
    },
});

let create_vendor_invoice_from_project_travel_request = function(frm){
    frm.call("create_vendor_invoice_from_project_travel_request").then((r) => {
        let vendor_invoice = r.message
        frappe.open_in_new_tab = true;
        frappe.set_route("Form", "Vendor Invoice", vendor_invoice);
       
    })
}