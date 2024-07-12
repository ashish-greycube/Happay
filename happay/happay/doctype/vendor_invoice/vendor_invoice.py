# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import today,get_link_to_form,nowdate
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account

class VendorInvoice(Document):
	def validate(self):
		self.validate_bill_amount()
		self.validate_posting_date()
		self.validate_tds_amount()
	
	def validate_bill_amount(self):
		if not self.bill_amount:
			frappe.throw(_("Please set bill amount"))
		elif self.bill_amount <= 0:
			frappe.throw(_("Bill amount cannot be zero or negative"))
	
	def validate_posting_date(self):
		posting_date = self.posting_date
		supplier_invoice_date = self.supplier_invoice_date
		if supplier_invoice_date > posting_date:
			frappe.throw(_("Supplier invoice date cannot be greater than posting date"))

	def validate_tds_amount(self):
		if self.tds_amount and self.bill_amount:
			bill_amount = self.bill_amount
			tds_amount = self.tds_amount
			if tds_amount > bill_amount:
				frappe.throw(_("TDS amount cannot be greater than bill amount"))

	def on_update(self):
		if self.workflow_state in ["Rejected by PM","Rejected By Fin 1"]:
			if self.rejection_remark==None or self.rejection_remark=="":
				frappe.throw(_("Please provide rejection remark"))

	def on_cancel(self):
		print("self.workflow_state",self.workflow_state)
		if self.workflow_state =="Rejected By Fin 2":
			if self.rejection_remark==None or self.rejection_remark=="":
				frappe.throw(_("Please provide rejection remark"))		

	def on_update_after_submit(self):
		if self.workflow_state=="To Pay":
			if self.type=='Invoice':
				user_roles = frappe.get_roles(frappe.session.user)
				if (("Accounts Manager" in user_roles) or ("Accounts User" in user_roles)):
					pi=create_purchase_invoice_from_vendor_invoice(docname=self.name)
					frappe.msgprint(_("Purchase Invoice {0} is created.").format(get_link_to_form("Purchase Invoice", pi)))	
				else:
					frappe.msgprint(_("You donot have required account roles to auto create Purchase Invoice from vendor invoice"))
				
			elif self.type=='Advance':
				user_roles = frappe.get_roles(frappe.session.user)
				if (("Accounts Manager" in user_roles) or ("Accounts User" in user_roles)):
					pe=make_payment_from_vendor_invoice(docname=self.name)
					frappe.msgprint(_("Payment Entry {0} is created.").format(get_link_to_form("Payment Entry", pe)))
				else:
					frappe.msgprint(_("You donot have required account roles to auto create Payment Entry from vendor invoice"))	

		if self.workflow_state=="Paid":
			if self.type=='Invoice':
				check_pi_exists = frappe.db.exists("Purchase Invoice", {"custom_vendor_invoice": self.name})
				if check_pi_exists == None:
					frappe.throw(_("Purchase invoice is not created, hence you cannot complete vendor invoice."))
				elif check_pi_exists:
					pi_status = frappe.db.get_value("Purchase Invoice",check_pi_exists,"docstatus")
					if pi_status == 0:
						frappe.throw(_("Purchase invoice {0} is in draft state, hence you cannot complete vendor invoice.").format(get_link_to_form("Purchase Invoice", check_pi_exists)))

			elif self.type=='Advance':
				check_pe_exists = frappe.db.exists("Payment Entry", {"custom_vendor_invoice": self.name})
				if check_pe_exists == None:
					frappe.throw(_("Payment entry is not created, hence you cannot complete vendor invoice."))
				elif check_pe_exists:
					pi_status = frappe.db.get_value("Payment Entry",check_pe_exists,"docstatus")
					if pi_status == 0:
						frappe.throw(_("Payment Entry {0} is in draft state, hence you cannot complete vendor invoice.").format(get_link_to_form("Payment Entry", check_pe_exists)))


@frappe.whitelist()
def create_purchase_invoice_from_vendor_invoice(docname):
	check_pi_exists = frappe.db.exists("Purchase Invoice", {"custom_vendor_invoice": docname})
	if check_pi_exists == None:
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

		tds_row = pi_doc.append("taxes",{})
		tds_row.add_deduct_tax = "Deduct"
		tds_row.charge_type = "Actual"
		tds_row.account_head = vi_doc.tds_payable_account
		tds_row.tax_amount = vi_doc.tds_amount
		tds_row.description = vi_doc.tds_payable_account

		pi_doc.run_method("set_missing_values")
		pi_doc.run_method("calculate_taxes_and_totals")
		pi_doc.save()

		return pi_doc.name
	else :
		frappe.msgprint(_("Purchase Invoice {0} is already exists for vendor invoice {1}").format(get_link_to_form("Purchase Invoice", check_pi_exists),docname))

@frappe.whitelist()
def make_payment_from_vendor_invoice(docname,target_doc=None):
	check_pe_exists = frappe.db.exists("Payment Entry", {"custom_vendor_invoice": docname})
	if check_pe_exists == None:
		vi_doc = frappe.get_doc("Vendor Invoice",docname)
		pe = frappe.new_doc("Payment Entry")
		pe.payment_type = "Pay"
		pe.company = vi_doc.company
		pe.cost_center = vi_doc.cost_center
		pe.posting_date = nowdate()
		pe.reference_date = nowdate()
		pe.paid_from = vi_doc.accounts_paid_from
		pe.party_type = "Supplier"
		pe.supplier = vi_doc.supplier
		pe.party = vi_doc.supplier
		pe.department = vi_doc.department
		pe.cost_center = vi_doc.cost_center
		pe.reference_no = vi_doc.supplier_invoice_number
		pe.party_account = get_party_account(pe.party_type ,pe.party,pe.company)

		company_default_payable_account = frappe.db.get_value("Company",vi_doc.company,"default_payable_account")
		default_company_currency = frappe.db.get_value("Company",vi_doc.company,"default_currency")
		if company_default_payable_account:
			pe.paid_to = company_default_payable_account
		if default_company_currency:
			pe.paid_to_account_currency = default_company_currency
		pe.custom_vendor_invoice = vi_doc.name
		pe.paid_amount = vi_doc.bill_amount
		pe.received_amount = vi_doc.bill_amount
		pe.party_bank_account = vi_doc.supplier_bank_account


		pe.run_method("setup_party_account_field")
		pe.run_method("set_missing_values")
		pe.run_method("set_missing_ref_details")
		pe.run_method("set_liability_account")
		pe.run_method("set_exchange_rate")
		pe.run_method("set_tax_withholding")
		pe.run_method("set_amounts")
		pe.run_method("set_status")
		pe.run_method("set_total_in_words")

		pe.save(ignore_permissions=True)
		return pe.name
	else :
		frappe.msgprint(_("Payment Entry {0} is already exists for vendor invoice {1}").format(get_link_to_form("Payment Entry", check_pe_exists),docname))

@frappe.whitelist()
def get_supplier_bank_account(supplier_name):
	supplier_default_bank_account = frappe.db.get_all("Bank Account",
												   filters={"party_type":"Supplier","party":supplier_name,"is_default":1})
	supplier_bank_account = frappe.db.get_all("Bank Account",
												   filters={"party_type":"Supplier","party":supplier_name})
	
	print(supplier_default_bank_account,"supplier_default_bank_account")
	print(supplier_bank_account,'supplier_bank_account')
	
	if len(supplier_default_bank_account)>0:
		return supplier_default_bank_account
	elif len(supplier_bank_account)>0:
		return supplier_bank_account

	