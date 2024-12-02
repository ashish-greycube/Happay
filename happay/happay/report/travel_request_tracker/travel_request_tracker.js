// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Travel Request Tracker"] = {
	"filters": [
		{
			"fieldname": "company",
			"label":__("Company"),
			"fieldtype": "Link",
			"options":"Company",
			"reqd":1
		},
		{
			"fieldname": "from_date",
			"label":__("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
		},
		{
			"fieldname": "to_date",
			"label":__("To Date"),
			"fieldtype": "Date",
            "default": frappe.datetime.nowdate()
		},
		{
			"fieldname": "project_travel_request",
			"label":__("Project Travel Request"),
			"fieldtype": "Link",
			"options": "Project Travel Request",
		},
	]
};
