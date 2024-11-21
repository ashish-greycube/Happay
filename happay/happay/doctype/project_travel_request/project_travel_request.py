# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today,getdate,get_link_to_form
from frappe.model.document import Document
from happay.happay.doctype.vendor_invoice.vendor_invoice import get_supplier_bank_account,get_supplier_bank_details,get_supplier_details


class ProjectTravelRequest(Document):
	def validate(self):
		self.validate_dates()

	def validate_dates(self):
		if self.from_date:
			print(self.from_date,"self.from_date",type(self.from_date))
			if getdate(self.from_date) < getdate(today()):
				frappe.throw(_("You cannot select from date before today"))
			if self.to_date:
				if self.to_date < self.from_date:
					frappe.throw(_("To date can not be less than From date"))

	@frappe.whitelist()
	def create_vendor_invoice_from_project_travel_request(self):
		vi_doc = frappe.new_doc("Vendor Invoice")
		vi_doc.company = self.company
		vi_doc.vendor_invoice_attachment_1 = self.ticket_attachment
		vi_doc.vendor_invoice_attachment_2 = self.invoice_attachment
		vi_doc.supplier = self.travel_agent
		vi_doc.posting_date = today()
		vi_doc.supplier_invoice_number = self.supplier_invoice_number
		vi_doc.supplier_invoice_date = self.supplier_invoice_date
		vi_doc.type = "Invoice"
		vi_doc.is_asset = "No"
		vi_doc.purpose = ""+self.name+","+self.title
		vi_doc.bill_amount = self.bill_amount
		vi_doc.expense_account = self.expense_account
		vi_doc.cost_center = self.cost_center
		vi_doc.project_manager = self.project_manager
		vi_doc.project_manager_name = self.project_manager_name

		supplier_bank_account = get_supplier_bank_account(self.travel_agent)
		vi_doc.supplier_bank_account = supplier_bank_account[0].name

		bank_details = get_supplier_bank_details(supplier_bank_account[0].name)
		print(bank_details,"bank_details")
		vi_doc.bank = bank_details.bank
		vi_doc.bank_account_no = bank_details.bank_account_no
		vi_doc.branch_code = bank_details.branch_code

		supplier_details = get_supplier_details(self.travel_agent)
		print(supplier_details,"supplier_details")
		vi_doc.tax_id = supplier_details.tax_id
		vi_doc.supplier_email = supplier_details.email_id
		vi_doc.department = self.department
		vi_doc.tds_amount = self.service_charge
		vi_doc.project_travel_request = self.name

		vi_doc.run_method("set_missing_values")
		vi_doc.save(ignore_permissions = True)
		frappe.msgprint(_("Vendor Invoice is created {0}".format(get_link_to_form("Vendor Invoice",vi_doc.name))),alert=True)
		return vi_doc.name

@frappe.whitelist()
def get_employee_detail(session_user):
	print(session_user,"frappe.session.user")
	employee_detail = frappe.db.get_value("Employee", {"user_id":session_user}, ["first_name","last_name","gender"],as_dict=1)
	print(employee_detail,"==================")
	return employee_detail
