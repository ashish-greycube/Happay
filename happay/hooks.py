app_name = "happay"
app_title = "Happay"
app_publisher = "GreyCube Technologies"
app_description = "HapPay"
app_email = "admin@greycube.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/happay/css/happay.css"
# app_include_js = "/assets/happay/js/happay.js"

# include js, css files in header of web template
# web_include_css = "/assets/happay/css/happay.css"
# web_include_js = "/assets/happay/js/happay.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "happay/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Expense Claim" : "public/js/expense_claim.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "happay/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "happay.utils.jinja_methods",
# 	"filters": "happay.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "happay.install.before_install"
# after_install = "happay.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "happay.uninstall.before_uninstall"
# after_uninstall = "happay.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "happay.utils.before_app_install"
# after_app_install = "happay.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "happay.utils.before_app_uninstall"
# after_app_uninstall = "happay.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "happay.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "Purchase Invoice": {
	# 	"on_submit": "happay.api.change_status_of_vendor_invoice_on_submit_of_purchase_invoice"
	# },
    "Payment Entry": {
        # "after_insert": "happay.api.change_status_of_vendor_invoice",
		"on_submit": ["happay.api.change_status_of_vendor_invoice",
                "happay.api.changes_status_of_expense_claim"]
	},
    "Cost Center": {
        "validate":"happay.api.create_custom_user_permission_for_project_manager"
	},
    "Expense Claim": {
        "validate":["happay.api.set_cost_center_in_all_row",
                    "happay.api.set_department_in_all_row",
                    "happay.api.validate_posting_date_and_expense_date"],
        "after_insert": "happay.api.share_expense_claim_to_employee"
	},
    "Employee": {
        "on_update":"happay.api.create_user_permission"
    },
    "Supplier": {
        "validate":"happay.api.validate_tax_id_length"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"happay.tasks.all"
# 	],
# 	"daily": [
# 		"happay.tasks.daily"
# 	],
# 	"hourly": [
# 		"happay.tasks.hourly"
# 	],
# 	"weekly": [
# 		"happay.tasks.weekly"
# 	],
# 	"monthly": [
# 		"happay.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "happay.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "happay.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "happay.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["happay.utils.before_request"]
# after_request = ["happay.utils.after_request"]

# Job Events
# ----------
# before_job = ["happay.utils.before_job"]
# after_job = ["happay.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"happay.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

website_route_rules = [{'from_route': '/get-travel-request-docs/<path:app_path>', 'to_route': 'get-travel-request-docs'},]