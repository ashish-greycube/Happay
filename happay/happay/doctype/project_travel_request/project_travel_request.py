# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today,getdate,get_link_to_form, cint
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from happay.happay.doctype.vendor_invoice.vendor_invoice import get_supplier_bank_account,get_supplier_bank_details,get_supplier_details
from frappe.model.workflow import apply_workflow
from frappe.model.docstatus import DocStatus


class ProjectTravelRequest(Document):
	def validate(self):
		self.validate_dates()
		self.validate_source_and_destination()
	
	def on_update(self):
		if self.workflow_state in ["Rejected","Rejected by PM"]:
			if self.rejection_remark==None or self.rejection_remark=="":
				frappe.throw(_("Please provide rejection remark"))

	def on_update_after_submit(self):
		self.changes_workflow_status_based_on_ticket_and_invoice()
		if self.workflow_state == "Billed":
			create_vendor_invoice_from_project_travel_request(self.name)

	def validate_dates(self):
		if self.trip_type in ["Round Trip","One Way"]:
			if self.from_date:
				if getdate(self.from_date) < getdate(today()):
					frappe.throw(_("You cannot select from date before today"))
			if self.trip_type == "Round Trip":
				if self.to_date:
					if self.to_date < self.from_date:
						frappe.throw(_("To date can not be less than From date"))
		if self.trip_type == "Multi Stop":
			if len(self.multi_stop_travel_details)>0:
				for row in self.multi_stop_travel_details:
					if getdate(row.travel_date) < getdate(today()):
						frappe.throw(_("Row #{0} :You cannot select travel date before today".format(row.idx)))
	
	def validate_source_and_destination(self):
		if self.trip_type in ["Round Trip","One Way"]:
			if self.source and self.destination:
				if self.destination == self.source:
					frappe.throw(_("Source and Destination can't be same"))
		if self.trip_type == "Multi Stop":
			if len(self.multi_stop_travel_details)>0:
				for row in self.multi_stop_travel_details:
					if row.source and row.destination:
						if row.source == row.destination:
							frappe.throw(_("# Row {0} : Source and Destination can't be same".format(row.idx)))
			
	def changes_workflow_status_based_on_ticket_and_invoice(self):
		print("in fun")
		if self.invoice_attachment:
			print("in condition")
			frappe.db.set_value(self.doctype,self.name,"workflow_state","Pending at Fin 1")

@frappe.whitelist()
def create_vendor_invoice_from_project_travel_request(name):
	ptr_doc = frappe.get_doc("Project Travel Request",name)
	vi_doc = frappe.new_doc("Vendor Invoice")
	vi_doc.company = ptr_doc.company
	vi_doc.vendor_invoice_attachment_1 = ptr_doc.invoice_attachment
	vi_doc.vendor_invoice_attachment_2 = ptr_doc.ticket_attachment
	vi_doc.supplier = ptr_doc.travel_agent
	vi_doc.posting_date = today()
	vi_doc.supplier_invoice_number = ptr_doc.supplier_invoice_number
	vi_doc.supplier_invoice_date = ptr_doc.supplier_invoice_date
	vi_doc.type = "Invoice"
	vi_doc.is_asset = "No"
	vi_doc.purpose = ""+ptr_doc.name+","+ptr_doc.reason_of_travel
	vi_doc.bill_amount = ptr_doc.bill_amount
	vi_doc.expense_account = ptr_doc.expense_account
	vi_doc.cost_center = ptr_doc.cost_center
	vi_doc.project_manager = ptr_doc.project_manager
	vi_doc.project_manager_name = ptr_doc.project_manager_name

	supplier_bank_account = get_supplier_bank_account(ptr_doc.travel_agent)
	vi_doc.supplier_bank_account = supplier_bank_account[0].name

	bank_details = get_supplier_bank_details(supplier_bank_account[0].name)
	print(bank_details,"bank_details")
	vi_doc.bank = bank_details.bank
	vi_doc.bank_account_no = bank_details.bank_account_no
	vi_doc.branch_code = bank_details.branch_code

	supplier_details = get_supplier_details(ptr_doc.travel_agent)
	print(supplier_details,"supplier_details")
	vi_doc.tax_id = supplier_details.tax_id
	vi_doc.supplier_email = supplier_details.email_id
	vi_doc.department = ptr_doc.department
	vi_doc.tds_amount = ptr_doc.service_charge
	vi_doc.project_travel_request = ptr_doc.name
	# vi_doc.workflow_state = "Pending at Fin 1"
	vi_doc.run_method("set_missing_values")
	vi_doc.save(ignore_permissions = True)
	# apply_workflow(frappe.get_doc("Vendor Invoice", vi_doc.name), "Submit")
	apply_workflow(frappe.get_doc("Vendor Invoice", vi_doc.name), "Approve")
	frappe.msgprint(_("Vendor Invoice is created {0}".format(get_link_to_form("Vendor Invoice",vi_doc.name))))
	return vi_doc.name
	
@frappe.whitelist()
def get_bill_amount(name):
	chagres = frappe.db.get_value("Project Travel Request",name,["bill_amount","service_charge"],as_dict=True)
	return chagres
		
@frappe.whitelist()
def get_employee_detail(session_user):
	print(session_user,"frappe.session.user")
	employee_detail = frappe.db.get_value("User", {"email":session_user}, ["first_name","last_name","gender","mobile_no"],as_dict=1)
	print(employee_detail,"==================")
	if employee_detail != None:
		if not employee_detail.last_name:
			frappe.throw(_("Please set last name in your profile"))
		if not employee_detail.gender:
			frappe.throw(_("Please set gender in your profile"))
		if not employee_detail.mobile_no:
			frappe.throw(_("Please set mobile number in your profile"))
	return employee_detail

@frappe.whitelist()
def create_expense_claim(source_name, target_doc=None):

	print(source_name,'source')

	def set_missing_values(source, target):
		target.company = source.company
		target.cost_center = source.cost_center
		target.custom_to_distribute_diff_cc = 0

	doc = get_mapped_doc(
		"Project Travel Request",
		source_name,
		{
			"Project Travel Request": {
				"doctype": "Expense Claim",
				"field_map": {"name": "custom_project_travel_request","project_manager":"expense_approver","department":"department"},
			}
		},
		target_doc,
		set_missing_values
	)

	doc.run_method("set_missing_values")
	return doc


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_travel_agent_group(doctype, txt, searchfield, start, page_len, filters):
		
		company = filters.get("company")
		supplier_group = frappe.db.get_single_value('Happay Settings', 'default_travel_agent_supplier_group')
		supplier_list = frappe.db.get_all("Supplier",
									filters={"supplier_group":supplier_group,"company":company},
									fields=["name","supplier_name","supplier_group"],as_list=1)

		return supplier_list

@frappe.whitelist()
def get_travel_agent_emails(travel_agent):
	travel_agent_emails = frappe.db.get_all("Supplier",
										 filters={"name":travel_agent},
										 fields=["email_id"])
	
	print(travel_agent_emails,'=============')
	return travel_agent_emails