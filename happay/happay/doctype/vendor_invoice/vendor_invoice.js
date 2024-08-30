// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor Invoice", {
    refresh(frm) {
        if (frm.is_new() == undefined && frappe.user.has_role('Projects Approver') && (frm.doc.workflow_state == "Pending at PM" || frm.doc.workflow_state =="Rejected by PM")) {
            let make_field_read_only = cint(1)
            for (const field of frm.meta.fields) {
                if (field.fieldname === "bill_amount" || field.fieldname ==="rejection_remark") {
                    frm.set_df_property(field.fieldname, "read_only", make_field_read_only ?0 : 1 );
                }else{
                    frm.set_df_property(field.fieldname, "read_only", make_field_read_only ?1 : 0 );
                }
            }
        }
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
        frm.set_query("expense_account", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "root_type":"Expense",
                    "is_group":0
                },
            }
        })        
        frm.set_query("supplier", function(doc){
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

        frm.set_query("cost_center", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "is_group":0
                },
            }
        })

        frm.set_query("tds_payable_account", function(doc) {
            var account_type = ["Tax", "Chargeable", "Income Account"];
            return {
                query: "happay.happay.doctype.vendor_invoice.vendor_invoice.tds_account_query",
                filters: {
                    "account_type": account_type,
                    "root_type":"Liability",
                    "company": doc.company,
                    "account_name": "%TDS%"
                }
            }
        });

        frm.set_query("advance_account", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "root_type":"Asset",
                    "is_group":0,
                    "account_name":["like", "Advance%"]
                },
            }
        })

        frm.set_query("asset_account", function(doc){
            return {
                filters: {
                    "company": doc.company,
                    "root_type":"Asset",
                    "is_group":0
                },
            }
        })
	},

    company(frm){
        let company = frm.doc.company
        frm.set_value("accounts_payable","")
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_payable_account_from_company",
            args: {
                "company": frm.doc.company
            },
            callback: function (response) {
                let payable_account = response.message
                if (payable_account){
                    frm.set_value("accounts_payable",payable_account.default_payable_account)
                }
            }
        })
    },

    cost_center(frm){
        let cost_center = frm.doc.cost_center
        frm.set_value("project_manager","")
        frm.set_value("project_manager_name","")
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_pm_and_account_from_cost_center",
            args: {
                "cost_center": frm.doc.cost_center
            },
            callback: function (response) {
                let cc_detials = response.message
                if (cc_detials){
                    frm.set_value("project_manager",cc_detials.custom_project_manager)
                    frm.set_value("project_manager_name",cc_detials.project_manager_name)
                }
            }
        })
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
                if (account_name.length > 0){
                    frm.set_value("supplier_bank_account",account_name[0].name)
                }
            }
        })
            
    },

    supplier_bank_account(frm){
        let supplier_bank_account = frm.doc.supplier_bank_account
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_supplier_bank_details",
            args: {
                "supplier_bank_account": supplier_bank_account
            },
            callback: function (response) {
                if (response.message){
                    frm.set_value("bank",response.message.bank)
                    frm.set_value("bank_account_no",response.message.bank_account_no)
                    frm.set_value("branch_code",response.message.branch_code)
                }
            }
        })
        let supplier_name = frm.doc.supplier
        frappe.call({
            method: "happay.happay.doctype.vendor_invoice.vendor_invoice.get_supplier_details",
            args: {
                "supplier_name": supplier_name
            },
            callback: function (response) {
                if (response.message){
                    frm.set_value("tax_id",response.message.tax_id)
                    frm.set_value("supplier_email",response.message.email_id)
                }
            }
        })

    },
    tds_amount(frm){
        frm.set_value("tds_computed_amount","")
        calculate_tds_computed_amount(frm)
    },

    tds_rate(frm){
        frm.set_value("tds_computed_amount","")
        calculate_tds_computed_amount(frm)
    },

    bill_amount(frm){
        calculate_net_payable_amount(frm)
    },

    tds_computed_amount(frm){
        calculate_net_payable_amount(frm)
    },

    before_save(frm){
        if (frm.doc.cost_center){
            if (frm.doc.project_manager==undefined || frm.doc.project_manager ==""){
                frappe.throw(__("Project manager is missing, please set project manager in parent cost center"))
            }
        }
        if (frm.doc.supplier){
            if (frm.doc.supplier_bank_account==undefined || frm.doc.supplier_bank_account ==""){
                frappe.throw(__("Please set bank account for supplier"))
            }
        }
    },
    before_workflow_action(frm){

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
                frappe.set_route("Form", "Payment Entry", response.message);
            }
        }
    });
}

function calculate_tds_computed_amount(frm){
    if(frm.doc.tds_amount && frm.doc.tds_rate){
        let computed_amount = (frm.doc.tds_amount * frm.doc.tds_rate) / 100
        frm.set_value("tds_computed_amount",computed_amount)
    }
}

function calculate_net_payable_amount(frm){
        let net_payable_amount = (frm.doc.bill_amount || 0) - (frm.doc.tds_computed_amount || 0)
        frm.set_value("net_payable_amount",net_payable_amount)
}