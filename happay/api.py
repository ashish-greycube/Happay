import frappe
from frappe import _

def change_status_of_vendor_invoice_on_submit_of_purchase_invoice(self,method):
    print("Ok")
    vi_number = frappe.db.get_value("Purchase Invoice",self.name,"custom_vendor_invoice")
    if vi_number:
        print(vi_number)
        vi_doc = frappe.get_doc("Vendor Invoice",vi_number)
        vi_doc.workflow_state = "To Pay"
        vi_doc.save()
        frappe.msgprint(_("Vendor Invoice's status changed to {0}").format(vi_doc.workflow_state),alert=1)

def change_status_of_vendor_invoice(self,method):
    # for  type invoice
    if len(self.references)>0 and method=="on_submit":
        for row in self.references:
            outstanding_amount_in_pi = frappe.db.get_value("Purchase Invoice",row.reference_name,"outstanding_amount")
            if outstanding_amount_in_pi == 0:
                vi_name_from_pi = frappe.db.get_value("Purchase Invoice",row.reference_name,"custom_vendor_invoice")
                if vi_name_from_pi :
                    vi_doc = frappe.get_doc("Vendor Invoice",vi_name_from_pi)
                    vi_doc.workflow_state = "Paid"
                    vi_doc.save()
                    frappe.msgprint(_("Vendor Invoice {0} status changed to {1}").format(vi_name_from_pi,vi_doc.workflow_state),alert=1)
    # for type advance 
    if self.custom_vendor_invoice :
        vi_doc = frappe.get_doc("Vendor Invoice",self.custom_vendor_invoice)
        if self.docstatus == 0 and method=="after_insert":
            vi_doc.workflow_state = "To Pay"
            vi_doc.save()
            frappe.msgprint(_("Vendor Invoice {0} status changed to {1}").format(self.custom_vendor_invoice,vi_doc.workflow_state),alert=1)
        if self.docstatus == 1 and method=="on_submit":
            vi_doc.workflow_state = "Paid"
            vi_doc.save()
            frappe.msgprint(_("Vendor Invoice {0} status changed to {1}").format(self.custom_vendor_invoice,vi_doc.workflow_state),alert=1)
