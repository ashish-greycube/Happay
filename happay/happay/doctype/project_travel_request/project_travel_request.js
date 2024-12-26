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
        frm.set_query("travel_agent", function () {
            return {
                query: "happay.happay.doctype.project_travel_request.project_travel_request.get_travel_agent_group",
                filters: {
                    "company": frm.doc.company
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

    onload_post_render(frm){
        make_all_fields_read_only(frm)
    },

    refresh(frm){
        make_all_fields_read_only(frm)
        frappe.call({
            method: "happay.happay.doctype.project_travel_request.project_travel_request.get_bill_amount",
            args: {
                "name": frm.doc.name
            },
            callback: function (response) {
                let details = response.message

                if (frm.doc.workflow_state == "Approved" && frm.doc.docstatus == 1 && details.bill_amount > 0 && details.service_charge > 0) {
                    frm.add_custom_button(__('Expense Claim'), () => create_expense_claim_from_project_travel_request(frm), __("Create"));
                }

                if (frm.doc.docstatus == 1 && details.bill_amount > 0 && details.service_charge > 0) {
                    frm.add_custom_button(__('Vendor Invoice'), () => create_vendor_invoice_from_project_travel_request(frm), __("Create"));
                }
            }
        })
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
    frappe.call({
        method: "happay.happay.doctype.project_travel_request.project_travel_request.create_vendor_invoice_from_project_travel_request",
        args: {
            "name": frm.doc.name
        },
        callback: function (response) {
            let vendor_invoice = response.message
            frappe.open_in_new_tab = true;
            frappe.set_route("Form", "Vendor Invoice", vendor_invoice);
        }
    })
}

let create_expense_claim_from_project_travel_request = function(frm) {
    console.log("----------")
    frappe.model.open_mapped_doc({
		method: "happay.happay.doctype.project_travel_request.project_travel_request.create_expense_claim",
		frm: frm,
	});
}

let make_all_fields_read_only = function(frm) {

    if (frappe.user.has_role('Projects Approver')) {
        frappe.model.with_doctype("Project Travel Request", function () {
            let meta = frappe.get_meta("Project Travel Request");
            meta.fields.forEach((value) => {
            console.log(value.fieldname)
            if (!["Section Break", "Column Break"].includes(value.fieldtype)) {
                    frm.set_df_property(value.fieldname, 'read_only', 1)
                }
            });
        });
    }
}