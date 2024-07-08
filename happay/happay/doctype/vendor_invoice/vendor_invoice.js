// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor Invoice", {
	setup(frm) {
        frm.set_query("supplier", function(doc){
            return {
                filters: {
                    "company": doc.company
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

        frm.set_query("department", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "is_group":0
                },
            }
        })

        frm.set_query("cost_center", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "is_group":0
                },
            }
        })
	},

    cost_center(frm){
        let cost_center = frm.doc.cost_center
        frappe.db.get_value("Cost Center",cost_center,"parent_cost_center").then(
            r => {
                frappe.db.get_value("Cost Center",r.message.parent_cost_center,"custom_project_manager").then(
                    value => {
                        frm.set_value("project_manager",value.message.custom_project_manager)
                    }
                )
            }
        )
    }
});
