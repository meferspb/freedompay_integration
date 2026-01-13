app_name = "freedompay_integration"
app_title = "FreedomPay Integration"
app_publisher = "Viktor Krasnikov"
app_description = "FreedomPay payment gateway integration for Frappe"
app_email = "vmk1981rus@gmail.com"
app_license = "MIT"

# App versions
app_version = "1.0.0"

# Required apps
required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/freedompay_integration/css/freedompay_integration.css"
# app_include_js = "/assets/freedompay_integration/js/freedompay_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/freedompay_integration/css/freedompay_integration_web.css"
# web_include_js = "/assets/freedompay_integration/js/freedompay_integration_web.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "freedompay_integration/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

before_install = "freedompay_integration.install.before_install"
after_install = "freedompay_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "freedompay_integration.uninstall.before_uninstall"
# after_uninstall = "freedompay_integration.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "freedompay_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"freedompay_integration.tasks.all"
#	],
#	"daily": [
#		"freedompay_integration.tasks.daily"
#	],
#	"hourly": [
#		"freedompay_integration.tasks.hourly"
#	],
#	"weekly": [
#		"freedompay_integration.tasks.weekly"
#	]
#	"monthly": [
#		"freedompay_integration.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "freedompay_integration.testing.before_tests"

# Overriding Methods
# ------------------------------
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "freedompay_integration.event.get_events"
# }
#
# each overriding function accepts a `data` parameter;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task" : "freedompay_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"filter_by": "{filter_by}",
#		"partial": 0,
#	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"freedompay_integration.auth.validate"
# ]
