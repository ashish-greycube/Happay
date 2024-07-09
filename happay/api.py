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

def change_status_of_vendor_invoice_on_submit_of_payment_entry(self,method):
    for row in self.references:
        outstanding_amount_in_pi = frappe.db.get_value("Purchase Invoice",row.reference_name,"outstanding_amount")
        if outstanding_amount_in_pi == 0:
            vi_name_from_pi = frappe.db.get_value("Purchase Invoice",row.reference_name,"custom_vendor_invoice")
            if vi_name_from_pi :
                vi_doc = frappe.get_doc("Vendor Invoice",vi_name_from_pi)
                vi_doc.workflow_state = "Paid"
                vi_doc.save()