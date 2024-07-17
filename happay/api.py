import frappe
from frappe import _
from frappe.permissions import add_user_permission
from frappe.utils import get_link_to_form
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


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def supplier_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	doctype = "Supplier"
	supp_master_name = frappe.defaults.get_user_default("supp_master_name")

	fields = ["name"]
	if supp_master_name != "Supplier Name":
		fields.append("supplier_name")

	fields = get_fields(doctype, fields)

	return frappe.db.sql(
		"""select {field} from `tabSupplier`
		where docstatus < 2
			and ({key} like %(txt)s
			or supplier_name like %(txt)s) and disabled=0
			and (on_hold = 0 or (on_hold = 1 and CURRENT_DATE > release_date))
			{mcond}
		order by
			(case when locate(%(_txt)s, name) > 0 then locate(%(_txt)s, name) else 99999 end),
			(case when locate(%(_txt)s, supplier_name) > 0 then locate(%(_txt)s, supplier_name) else 99999 end),
			idx desc,
			name, supplier_name
		limit %(page_len)s offset %(start)s""".format(
			**{"field": ", ".join(fields), "key": searchfield, "mcond": get_match_cond(doctype)}
		),
		{"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
		as_dict=as_dict,
	)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def customer_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	doctype = "Customer"
	conditions = []
	cust_master_name = frappe.defaults.get_user_default("cust_master_name")

	fields = ["name"]
	if cust_master_name != "Customer Name":
		fields.append("customer_name")

	fields = get_fields(doctype, fields)
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	return frappe.db.sql(
		"""select {fields} from `tabCustomer`
		where docstatus < 2
			and ({scond}) and disabled=0
			{fcond} {mcond}
		order by
			(case when locate(%(_txt)s, name) > 0 then locate(%(_txt)s, name) else 99999 end),
			(case when locate(%(_txt)s, customer_name) > 0 then locate(%(_txt)s, customer_name) else 99999 end),
			idx desc,
			name, customer_name
		limit %(page_len)s offset %(start)s""".format(
			**{
				"fields": ", ".join(fields),
				"scond": searchfields,
				"mcond": get_match_cond(doctype),
				"fcond": get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
			}
		),
		{"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
		as_dict=as_dict,
	)

def get_fields(doctype, fields=None):
	if fields is None:
		fields = []
	meta = frappe.get_meta(doctype)
	fields.extend(meta.get_search_fields())

	if meta.title_field and meta.title_field.strip() not in fields:
		fields.insert(1, meta.title_field.strip())

	return unique(fields)