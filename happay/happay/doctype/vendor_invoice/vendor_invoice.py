# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import today
from erpnext.accounts.party import get_party_account

class VendorInvoice(Document):
	def validate(self):
		self.validate_bill_amount()
	
	def validate_bill_amount(self):
		if not self.bill_amount:
			frappe.throw(_("Please set bill amount"))
		elif self.bill_amount <= 0:
			frappe.throw(_("Bill amount cannot be zero or negative"))

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
	pi_doc.bill_no = vi_doc.supplier_invoice_number
	pi_doc.bill_date = vi_doc.supplier_invoice_date

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

@frappe.whitelist()
def make_payment_from_vendor_invoice(docname,target_doc=None):
	print("PE")
	vi_doc = frappe.get_doc("Vendor Invoice",docname)
	def set_missing_values(source, target):
		# po_doc = frappe.new_doc("Purchase Order")
		# target.supplier = vi_doc.supplier
		# target.company = vi_doc.company
		# po_doc.custom_vendor_invoice = vi_doc.name
		# target.cost_center = vi_doc.cost_center
		# target.department = vi_doc.department
		target.payment_type = "Pay"
		target.party_type = "Supplier"
		target.company = vi_doc.company
		target.party = vi_doc.supplier
		target.party_bank_account = vi_doc.supplier_bank_account
		target.paid_amount = vi_doc.bill_amount
		target.supplier = vi_doc.supplier
		target.department = vi_doc.department
		target.cost_center = vi_doc.cost_center
		target.reference_no = vi_doc.supplier_invoice_number
		target.reference_date = today()
		target.posting_date = today()
		target.party_account = get_party_account(target.party_type ,target.party,target.company)

	doc = get_mapped_doc('Vendor Invoice', vi_doc, {
		'Vendor Invoice': {
			'doctype': 'Payment Entry',
			# 'field_map': {
			# 	'supplier_invoice_number':'reference_no'
			# },			
			'validation': {
				'docstatus': ['!=', 2]
			}
		}	
	}, target_doc,set_missing_values)
	doc.run_method("onload")
	doc.run_method("set_missing_values")

	return doc
