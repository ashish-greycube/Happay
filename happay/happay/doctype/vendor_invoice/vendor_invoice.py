# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
import erpnext
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import today,get_link_to_form,nowdate,formatdate
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from frappe.desk.reportview import get_filters_cond, get_match_cond

class VendorInvoice(Document):
	def validate(self):
		self.validate_bill_amount()
		self.validate_posting_date()
		self.validate_tds_amount()
	
	def validate_bill_amount(self):
		if self.bill_amount <= 0:
			frappe.throw(_("Bill amount cannot be zero or negative"))
		if self.workflow_state !="Draft":
			old_doc = self.get_doc_before_save()
			if self.bill_amount > old_doc.bill_amount:
				frappe.throw(_("Bill amount entered is {0}. It cannot be greater than {1}".format(self.bill_amount ,old_doc.bill_amount)))
	
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
					je=create_journal_entry_from_vendor_invoice(docname=self.name)
					frappe.msgprint(_("Journal Entry {0} is created.").format(get_link_to_form("Journal Entry", je)))
				else:
					frappe.msgprint(_("You donot have required account roles to auto create Journal Entry from vendor invoice"))	

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
				check_pe_exists = frappe.db.exists("Journal Entry", {"custom_vendor_invoice": self.name})
				if check_pe_exists == None:
					frappe.throw(_("Journal entry is not created, hence you cannot complete vendor invoice."))
				elif check_pe_exists:
					pi_status = frappe.db.get_value("Journal Entry",check_pe_exists,"docstatus")
					if pi_status == 0:
						frappe.throw(_("Journal Entry {0} is in draft state, hence you cannot complete vendor invoice.").format(get_link_to_form("Payment Entry", check_pe_exists)))


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
		pi_original_remarks = _("Against Supplier Invoice {0} dated {1}").format(pi_doc.bill_no, formatdate(pi_doc.bill_date))		
		pi_doc.remarks = pi_original_remarks+'\n'+vi_doc.purpose
		pi_doc.posting_date=vi_doc.posting_date
		pi_doc.set_posting_time=1

		row = pi_doc.append("items",{})
		row.item_name = vi_doc.purpose
		row.qty = 1
		row.uom = "Nos"
		row.rate = vi_doc.bill_amount
		row.expense_account = vi_doc.expense_account
		row.cost_center = vi_doc.cost_center
		row.department = vi_doc.department
		row.description = vi_doc.purpose

		if vi_doc.is_tds_applicable==1:
			tds_row = pi_doc.append("taxes",{})
			tds_row.add_deduct_tax = "Deduct"
			tds_row.charge_type = "Actual"
			tds_row.account_head = vi_doc.tds_payable_account
			tds_row.tax_amount = vi_doc.tds_amount
			tds_row.description = vi_doc.tds_payable_account
			tds_row.cost_center = vi_doc.cost_center
			tds_row.department = vi_doc.department

		pi_doc.run_method("set_missing_values")
		pi_doc.run_method("calculate_taxes_and_totals")
		pi_doc.save()

		return pi_doc.name
	else :
		frappe.msgprint(_("Purchase Invoice {0} is already exists for vendor invoice {1}").format(get_link_to_form("Purchase Invoice", check_pi_exists),docname))

@frappe.whitelist()
def create_journal_entry_from_vendor_invoice(docname,target_doc=None):
	
	vi_doc = frappe.get_doc("Vendor Invoice",docname)
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.company = vi_doc.company
	je.posting_date = vi_doc.posting_date
	je.user_remark = vi_doc.purpose
	je.cheque_no = vi_doc.supplier_invoice_number
	je.cheque_date = vi_doc.supplier_invoice_date
	je.pay_to_recd_from = vi_doc.supplier
	je.custom_vendor_invoice = vi_doc.name
	
	accounts = []
	accounts.append({
		"account":vi_doc.advance_account,
		"cost_center":vi_doc.cost_center,
		"department":vi_doc.department,
		"supplier":vi_doc.supplier,
		"debit_in_account_currency":vi_doc.bill_amount,
		"is_advance": "Yes"
	})
	accounts.append({
		"account":vi_doc.tds_payable_account,
		"cost_center":vi_doc.cost_center,
		"department":vi_doc.department,
		"supplier":vi_doc.supplier,
		"credit_in_account_currency":vi_doc.tds_amount
	})
	company_default_payable_account = frappe.db.get_value("Company",vi_doc.company,"default_payable_account")
	accounts.append({
		"account":company_default_payable_account,
		"cost_center":vi_doc.cost_center,
		"department":vi_doc.department,
		"supplier":vi_doc.supplier,
		"party_type": "Supplier",
		"party": vi_doc.supplier,
		"credit_in_account_currency":vi_doc.bill_amount - vi_doc.tds_amount
	})
	je_row = je.set("accounts",accounts)
	je.run_method('set_missing_values')
	je.save()
	je.add_comment("Comment", "Journal Entry is created for Vendor Invoice {0}".format(get_link_to_form("Vendor Invoice", vi_doc.name)))
	return je.name

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


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def tds_account_query(doctype, txt, searchfield, start, page_len, filters):
	doctype = "Account"
	company_currency = erpnext.get_company_currency(filters.get("company"))

	def get_accounts(with_account_type_filter):
		account_type_condition = ""
		if with_account_type_filter:
			account_type_condition = "AND account_type in %(account_types)s"

		accounts = frappe.db.sql(
			f"""
			SELECT name, parent_account
			FROM `tabAccount`
			WHERE `tabAccount`.docstatus!=2
				{account_type_condition}
				AND is_group = 0
				AND company = %(company)s
				AND disabled = %(disabled)s
				AND (account_currency = %(currency)s or ifnull(account_currency, '') = '')
				AND account_name LIKE %(account_name)s
				AND `{searchfield}` LIKE %(txt)s
				{get_match_cond(doctype)}
			ORDER BY idx DESC, name
			LIMIT %(limit)s offset %(offset)s
		""",
			dict(
				account_types=filters.get("account_type"),
				company=filters.get("company"),
				disabled=filters.get("disabled", 0),
				currency=company_currency,
				account_name=filters.get("account_name"),
				txt=f"%{txt}%",
				offset=start,
				limit=page_len,
			),debug = 1
		)

		return accounts

	tax_accounts = get_accounts(True)

	if not tax_accounts:
		tax_accounts = get_accounts(False)

	return tax_accounts
	