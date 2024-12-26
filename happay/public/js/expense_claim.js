frappe.ui.form.on("Expense Claim", {

    refresh(frm){
        frm.remove_custom_button('Payment', 'Create');  
        set_feilds_as_readonly_for_fin1_fin2_role(frm)
    },
    onload_post_render(frm){
        if (!frm.doc.employee){
            frm.set_value("custom_project_travel_request","")
        }
        set_feilds_as_readonly_for_fin1_fin2_role(frm)
    },
    after_workflow_action(frm){
        let method = "hrms.overrides.employee_payment_entry.get_payment_entry_for_employee";
        if (frm.doc.workflow_state == "In Process"){
            return frappe.call({
                method: method,
                args: {
                    dt: frm.doc.doctype,
                    dn: frm.doc.name,
                },
                callback: function (r) {
                    var doclist = frappe.model.sync(r.message);
                    frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
                },
            });
        }
    },

    onload(frm){
        if (frm.is_new()){
            frappe.call({
                method: "happay.api.fetch_logged_in_user_employee",
                args: {
                    "session_user": frappe.session.user
                },
                callback: function (response) {
                    let emp_detials = response.message
                    if (emp_detials) {
                        frm.set_value("employee", emp_detials)
                    }
                }
            })

            if (frappe.user.has_role('Projects Manager')) {
                frappe.db.get_value("Employee",{user_id:frappe.session.user},["expense_approver"])
                .then(r => {
                    let expense_approver = r.message.expense_approver
                    frm.set_value("expense_approver", expense_approver)
                })
            }
        }
    },

    cost_center(frm) {
        let user_role_list = frappe.user_roles
        if (frappe.user.has_role('Projects Approver')) {
            frappe.db.get_value("Employee",{user_id:frappe.session.user},["expense_approver"])
            .then(r => {
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
    },

    company(frm) {
        console.log("accounnttt")
        frappe.db.get_value("Company",frm.doc.company,["default_expense_claim_payable_account"])
            .then(r => {
                console.log(r.message,"payable account")
                let default_expense_claim_payable_account = r.message.default_expense_claim_payable_account
                frm.set_value("payable_account", default_expense_claim_payable_account)
            })
    },

    make_payment_entry: function (frm) {
		let method = "hrms.overrides.employee_payment_entry.get_payment_entry_for_employee";
		if (frm.doc.__onload && frm.doc.__onload.make_payment_via_journal_entry) {
			console.log("-------------")
			method = "hrms.hr.doctype.expense_claim.expense_claim.make_bank_entry";
		}
		console.log(method)
		return frappe.call({
			method: method,
			args: {
				dt: frm.doc.doctype,
				dn: frm.doc.name,
			},
			callback: function (r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			},
		});
	},
})


function set_feilds_as_readonly_for_fin1_fin2_role(frm) {
    if ((frappe.user.has_role("Fin 1") || frappe.user.has_role("'Fin 2")) && !frappe.user.has_role("Administrator")){
        frappe.model.with_doctype("Expense Claim Detail", function () {
            let meta = frappe.get_meta("Expense Claim Detail");
            meta.fields.forEach((value) => {
                if (!["Section Break", "Column Break"].includes(value.fieldtype)) {
                    if (!["amount", "sanctioned_amount"].includes(value.fieldname)) {
                        frm.fields_dict["expense_details"].grid.update_docfield_property(value.fieldname, read_only, 1);
                        frm.set_df_property(value.fieldname, 'read_only', 1)
                    }
                    if (["amount", "sanctioned_amount"].includes(value.fieldname)) {
                        frm.fields_dict["expense_details"].grid.update_docfield_property(value.fieldname, read_only, 0);
                        console.log(value.fieldname, "===========")
                    }                        
                }
            });
        });
    }    
}