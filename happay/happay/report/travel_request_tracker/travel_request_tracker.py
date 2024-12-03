# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):
	return [
		{
			"fieldname": "travel_request",
			"label":_("Travel Request"),
			"fieldtype": "Link",
			"options": "Project Travel Request",
			"width":"150"
		},
		{
			"fieldname": "company",
			"label":_("Company"),
			"fieldtype": "Link",
			"options":"Company"
		},
		{
			"fieldname": "cost_center",
			"label":_("Cost Center"),
			"fieldtype": "Link",
			"options":"Cost Center",
			"width":"180"
		},
		{
			"fieldname": "title",
			"label":_("Title"),
			"fieldtype": "Data",
			"width":"130"
		},
		{
			"fieldname": "employee",
			"label":_("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"width":"150"
		},
		{
			"fieldname": "employee_name",
			"label":_("Employee Name"),
			"fieldtype": "Data",
			"width":"140"
		},
		{
			"fieldname": "expense_claim",
			"label":_("Expense Claim"),
			"fieldtype": "Link",
			"options":"Expense Claim",
			"width":"130"
		},
		{
			"fieldname": "expense_amount",
			"label":_("Expense Amount"),
			"fieldtype": "Currency",
			"width":"130"
		},
		{
			"fieldname": "paid_amount",
			"label":_("Paid Amount"),
			"fieldtype": "Currency",
			"width":"130"
		},
		{
			"fieldname": "outstanding_amount",
			"label":_("Outstanding Amount"),
			"fieldtype": "Currency",
			"width":"130"
		},
		{
			"fieldname": "vendor_invoice",
			"label":_("Vendor Invoice"),
			"fieldtype": "Link",
			"options":"Vendor Invoice",
			"width":"130"
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)

	report_data = frappe.db.sql("""
				SELECT
					ptr.name as travel_request ,
					ptr.company ,
					ptr.cost_center ,
					ptr.title ,
					ec.employee ,
					ec.employee_name,
					ec.name as expense_claim ,
					ec.grand_total as expense_amount ,
					ec.total_amount_reimbursed as paid_amount ,
					(ec.grand_total - ec.total_amount_reimbursed) as outstanding_amount ,
					vi.name as vendor_invoice
				FROM
					`tabProject Travel Request` as ptr
				LEFT OUTER JOIN `tabExpense Claim` as ec on
					ptr.name = ec.custom_project_travel_request
				LEFT OUTER JOIN `tabVendor Invoice` as vi on
					ptr.name = vi.project_travel_request
					where ptr.docstatus = 1 and
					{0}
		""".format(conditions),filters,as_dict=1,debug=1)
	
	return report_data

def get_conditions(filters):
	print(filters)
	conditions = ""
	if filters.company:
		conditions += "ptr.company = %(company)s"

	if filters.from_date:
		conditions += "and ptr.from_date >= %(from_date)s"
	
	if filters.to_date:
		conditions += "and ptr.from_date <= %(to_date)s"

	if filters.project_travel_request:
		conditions += "and ptr.name = %(project_travel_request)s"

	print(conditions,"--")
	return conditions