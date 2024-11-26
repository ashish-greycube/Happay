import frappe
from frappe import _
from frappe.permissions import add_user_permission
from frappe.utils import get_link_to_form
from frappe.model.mapper import get_mapped_doc
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique

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
		result = add_user_permission(doctype="User",user=self.custom_project_manager,name=self.custom_project_manager,applicable_for="Vendor Invoice",ignore_permissions=True)
		check_exist = frappe.db.exists("User Permission", {"user":self.custom_project_manager,"applicable_for":"Vendor Invoice"})
		print(check_exist,"permission")
		if check_exist != None:
			frappe.msgprint(_("User Permission {0} is added ").format(get_link_to_form("User Permission", check_exist)))

def set_cost_center_in_all_row(self, method):
	if len(self.expenses)>0:
		for row in self.expenses:
			row.cost_center = self.cost_center

@frappe.whitelist()
def fetch_logged_in_user_employee(session_user):
	employee_detail = frappe.db.get_value("Employee", {"user_id":session_user}, ["name"],as_dict=1)
	if employee_detail:
		return employee_detail.name

# def changes_status_of_expense_claim(self, method):
# 	if len(self.references)>0 and method=="on_submit":
# 		for row in self.references:
# 			if row.reference_doctype == "Expense Claim":
# 				ec_doc = frappe.get_doc("Expense Claim",row.reference_name)
# 				ec_doc.workflow_state = "Paid"
# 				ec_doc.save()
# 				frappe.msgprint(_("Expense Claim {0} status changed to {1}").format(row.reference_name,ec_doc.workflow_state),alert=1)