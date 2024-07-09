# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VendorInvoice(Document):
	pass

@frappe.whitelist()
def create_purchase_invoice_from_vendor_invoice(docname):
	print("PI")
	vi_doc = frappe.get_doc("Vendor Invoice",docname)
	pi_doc = frappe.new_doc("Purchase Invoice")
	pi_doc.supplier = vi_doc.supplier
	pi_doc.company = vi_doc.company
	pi_doc.custom_vendor_invoice = vi_doc.name
	pi_doc.cost_center = vi_doc.cost_center
	pi_doc.department = vi_doc.department

	row = pi_doc.append("items",{})
	row.item_name = vi_doc.purpose
	row.qty = 1
	row.uom = "Nos"
	row.rate = vi_doc.bill_amount
	row.expense_account = vi_doc.expense_account
	row.cost_center = vi_doc.cost_center
	row.department = vi_doc.department
	row.description = vi_doc.purpose

	pi_doc.run_method("set_missing_values")
	pi_doc.run_method("calculate_taxes_and_totals")
	pi_doc.save()

	return pi_doc.name