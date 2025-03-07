import frappe
from frappe import _
from frappe.permissions import add_user_permission
from frappe.utils import get_link_to_form, add_to_date, getdate, today, flt
from frappe.model.mapper import get_mapped_doc
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique
from frappe.share import add

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

def create_custom_user_permission_for_project_manager(self,method):
	if self.is_group==1 and self.custom_project_manager:
		permission_for_vi = add_user_permission(doctype="User",user=self.custom_project_manager,name=self.custom_project_manager,applicable_for="Vendor Invoice",ignore_permissions=True)
		# permission_for_ptr = add_user_permission(doctype="User",user=self.custom_project_manager,name=self.custom_project_manager,applicable_for="Project Travel Request",ignore_permissions=True)
		check_exist_for_vi = frappe.db.exists("User Permission", {"user":self.custom_project_manager,"applicable_for":"Vendor Invoice"})
		# check_exist_for_ptr = frappe.db.exists("User Permission", {"user":self.custom_project_manager,"applicable_for":"Project Travel Request"})
		
		if check_exist_for_vi != None:
			frappe.msgprint(_("User Permission {0} is added for Vendor Invoice").format(get_link_to_form("User Permission", check_exist_for_vi)),alert=True)
		# if check_exist_for_ptr != None:
		# 	frappe.msgprint(_("User Permission {0} is added Project Travel Request").format(get_link_to_form("User Permission", check_exist_for_ptr)),alert=True)

def set_cost_center_in_all_row(self, method):
	if self.custom_to_distribute_diff_cc == 0:
		if len(self.expenses)>0:
			for row in self.expenses:
				row.cost_center = self.cost_center

@frappe.whitelist()
def fetch_logged_in_user_employee(session_user):
	employee_detail = frappe.db.get_value("Employee", {"user_id":session_user}, ["name"],as_dict=1)
	if employee_detail:
		return employee_detail.name

def changes_status_of_expense_claim(self, method):
	if len(self.references)>0 and method=="on_submit":
		for row in self.references:
			if row.reference_doctype == "Expense Claim":
				ec_doc = frappe.get_doc("Expense Claim",row.reference_name)
				ec_doc.workflow_state = "Paid"
				ec_doc.save()
				frappe.msgprint(_("Expense Claim {0} status changed to {1}").format(row.reference_name,ec_doc.workflow_state),alert=1)

def share_expense_claim_to_employee(self,method):

	user_list = frappe.db.get_all("User",
							   filters={"enabled":1},
							   fields=["name"])
	required_user_list = []
	for user in user_list:
		user_roles = frappe.get_roles(user.name)
		if (('Fin 1' in user_roles) or ('Fin 2' in user_roles)) and user.name != 'Administrator':
			required_user_list.append(user.name)
	
	for user_id in required_user_list:
		shared_with_user=add(self.doctype, self.name, user=user_id, read=1, write=1, submit=1)
		if shared_with_user:
				frappe.msgprint(
					_("Expense Claim {0} is shared with {1} user").format(self.name,user_id),
					alert=1,
				)
			
def validate_posting_date_and_expense_date(self, method):
	
	valide_date = add_to_date(nowdate(),days=-30)
	if self.posting_date and getdate(self.posting_date) < getdate(valide_date):
		frappe.throw(_("Posting cannot be less then {0}".format(valide_date)))
	if len(self.expenses)>0:
		for row in self.expenses:
			if row.expense_date and getdate(row.expense_date) < getdate(valide_date):
				frappe.throw(_("#Row {0}: Expense date cannot be less then {1}".format(row.idx,valide_date)))

	minimum_expense_date = None
	if len(self.expenses)>0:
		for row in self.expenses:
			if minimum_expense_date==None:
				minimum_expense_date = row.expense_date
			if row.expense_date < minimum_expense_date:
				minimum_expense_date = row.expense_date

	if getdate(self.posting_date) < getdate(minimum_expense_date):
		frappe.throw(_("Posting date cannot be less than minimum expense date {0}".format(minimum_expense_date)))

def create_user_permission(self, method):

	if self.user_id:
		user_roles = frappe.get_roles(self.user_id)
		if "Finance Team" not in user_roles:
			employee_user_permission_exists = frappe.db.exists(
					"User Permission", {"allow": "Employee", "for_value": self.name, "user": self.user_id}
				)
			if employee_user_permission_exists:
				return
			else :
				add_user_permission("Employee", self.name, self.user_id)
				frappe.msgprint(_("User permissions for Employee is created"),alert=True)

def set_department_in_all_row(self, method):
	if len(self.expenses)>0:
		for row in self.expenses:
			row.department = self.department

def validate_tax_id_length(self, method):
	if self.tax_id:
		print(len(self.tax_id),"tax_id")
		if len(self.tax_id) != 10:
			frappe.throw(_("Tax ID must be of 10 digits"))

def validate_amount_and_sanctioned_amount(self, method):
	if len(self.expenses)>0:
		for row in self.expenses:
			print(row.amount,type(row.amount),flt(row.amount) < flt(1),flt(row.amount),flt(1))
			if (flt(row.amount) < flt(1)):
				frappe.throw(_("#Row {0}: Amount must be greater then zero".format(row.idx)))
	
	if self.workflow_state !="Draft":
			old_doc = self.get_doc_before_save()
			if old_doc:
				if len(old_doc.expenses)>0:
					for old_row in old_doc.expenses:
						for new_row in self.expenses:
							if new_row.name == old_row.name:
								if new_row.sanctioned_amount > old_row.sanctioned_amount:
									frappe.throw(_("#Row {0}: Sanctioned Amount entered is {1}. It cannot be greater than {2}".format(new_row.idx,new_row.sanctioned_amount ,old_row.sanctioned_amount)))

def update_posting_date_based_on_approval(self,method):
	user_roles = frappe.get_roles(frappe.session.user)
	if ("Projects Approver" in user_roles):
		if self.workflow_state in ["Pending at Fin 1"]:
			frappe.db.set_value("Expense Claim",self.name,"posting_date",getdate(today()))
		
def add_rejection_remark_for_rejection(self,method):
	if self.workflow_state in ["Rejected By Fin 1","Rejected by PM","Rejected By Fin 2"]:
		if self.custom_rejection_remark==None or self.custom_rejection_remark=="":
			frappe.throw(_("Please provide rejection remark"))

def set_expense_claim_in_attached_file(self, method):
	# https://github.com/frappe/frappe/pull/30883
	if len(self.expenses):
		for row in self.expenses:
			if row.custom_bill_attachment:
				get_file_id = frappe.db.get_all("File",
									filters={"file_url":row.custom_bill_attachment,"attached_to_name":["like",f"%new-expense-claim%"]},
									fields=["name","attached_to_name"])
				if len(get_file_id)>0:
					frappe.db.set_value("File",get_file_id[0].name,"attached_to_name",self.name)