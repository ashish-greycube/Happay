frappe.ui.form.on("Expense Claim", {
    cost_center(frm) {
        let user_role_list = frappe.user_roles
        if (frappe.user.has_role('Projects Manager')) {
            frappe.db.get_value("Employee",{user_id:frappe.session.user},["expense_approver"])
            .then(r => {
                console.log(r)
                let expense_approver = r.message.expense_approver
                frm.set_value("expense_approver", expense_approver)
            })
        }
        else {
            frappe.call({
                method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_pm_and_account_from_cost_center",
                args: {
                    "cost_center": frm.doc.cost_center
                },
                callback: function (response) {
                    let cc_detials = response.message
                    if (cc_detials) {
                        frm.set_value("expense_approver", cc_detials.custom_project_manager)
                    }
                }
            })
        }
    }
})