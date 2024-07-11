// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor Invoice", {
    refresh(frm){
        frm.trigger("vendon_invoice_on_refresh_load")
    },
    vendon_invoice_on_refresh_load : function(frm){
        if (frm.doc.docstatus == 1 && frm.doc.workflow_state == "To Account" && frappe.user.has_role(["Accounts Manager", "Accounts User"])) {
            if (frm.doc.type == "Invoice"){
                frm.add_custom_button(__('Purchase Invoice'), () => create_purchase_invoice_from_vendor_invoice(frm), __("Create"));
            }
            else if (frm.doc.type == "Advance") {
                frm.add_custom_button(__('Payment'), () => make_payment_from_vendor_invoice(frm), __("Create"));
            }
        }
    },
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
        frm.set_value("project_manager","")
        frappe.db.get_value("Cost Center",cost_center,"parent_cost_center").then(
            r => {
                frappe.db.get_value("Cost Center",r.message.parent_cost_center,"custom_project_manager").then(
                    value => {
                            frm.set_value("project_manager",value.message.custom_project_manager)
                        
                    }
                )
            }
        )
    },

    supplier(frm){
        let supplier_name = frm.doc.supplier
        frm.set_value("supplier_bank_account","")
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_supplier_bank_account",
            args: {
                "supplier_name": supplier_name
            },
            callback: function (response) {
                let account_name = response.message
                console.log(account_name)
                if (account_name != undefined){
                    frm.set_value("supplier_bank_account",account_name[0].name)
                }
            }
        })
            
    },
    before_save(frm){
        if (frm.doc.project_manager==undefined || frm.doc.project_manager ==""){
            frappe.throw(__("Project manager is missing, please set project manager in parent cost center"))
        }
        if (frm.doc.supplier_bank_account==undefined || frm.doc.supplier_bank_account ==""){
            frappe.throw(__("Please set bank account for supplier"))
        }
    }
});


function create_purchase_invoice_from_vendor_invoice(frm){
    frappe.call({
        method: "happay.happay.doctype.vendor_invoice.vendor_invoice.create_purchase_invoice_from_vendor_invoice",
        args: {
            "docname": frm.doc.name
        },
        callback: function (response) {
            if (response.message) {
                let url_list = '<a href="/app/purchase-invoice/' + response.message + '" target="_blank">' + response.message + '</a><br>'
                frappe.msgprint({
                    title: __('Notification'),
                    message: __('Purchase Invoice is created ' + url_list),
                    indicator: 'green'
                }, 12);
                window.open(`/app/purchase-invoice/` + response.message);
            }
        }
    });
}

function make_payment_from_vendor_invoice(frm){
    frappe.call({
        method: "happay.happay.doctype.vendor_invoice.vendor_invoice.make_payment_from_vendor_invoice",
        args: {
            "docname": frm.doc.name
        },
        callback: function (response) {
            if (response.message) {
				var doc = frappe.model.sync(response.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
            }
        }
    });
}