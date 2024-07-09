// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor Invoice", {
    refresh(frm){
        frm.trigger("vendon_invoice_on_refresh_load")
    },
    vendon_invoice_on_refresh_load : function(frm){
        if (frm.doc.docstatus == 1 && frm.doc.workflow_state == "To Account") {
            if (frm.doc.type == "Invoice"){
                frm.add_custom_button(__('Purchase Invoice'), () => create_purchase_invoice_from_vendor_invoice(frm), __("Create"));
            }
            else {
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
        frappe.db.get_value("Cost Center",cost_center,"parent_cost_center").then(
            r => {
                frappe.db.get_value("Cost Center",r.message.parent_cost_center,"custom_project_manager").then(
                    value => {
                        if (value.message.custom_project_manager==undefined){
                            frm.set_value("project_manager","")
                            frappe.throw(__("Please set project manager in {0}",[r.message.parent_cost_center]))
                        }
                        frm.set_value("project_manager",value.message.custom_project_manager)
                    }
                )
            }
        )
    },

    supplier(frm){
        let supplier_name = frm.doc.supplier
        console.log(supplier_name)
        frappe.db.get_list('Bank Account', {
            filters : {party_type:'Supplier', party: supplier_name, is_default:1},
            fields : ['name']
        }).then(records => {
            if (records.length > 0){
                console.log("default")
                frm.set_value("supplier_bank_account",records[0].name)
            }
            else{
                frappe.db.get_list('Bank Account', {
                    filters : {party_type:'Supplier', party: supplier_name},
                    fields : ['name']
                }).then(records => {
                    if (records.length > 0){
                        frm.set_value("supplier_bank_account",records[0].name)
                    }
                    else{
                        frappe.throw(__("Please set bank account for supplier"))
                    }
                })
            }
        })
            
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