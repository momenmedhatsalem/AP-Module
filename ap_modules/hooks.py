app_name = "ap_modules"
app_title = "AP Modules"
app_publisher = "Momen Medhat"
app_description = "Adds requests and base64 to the Server Script NameSpaces"
app_email = "momenmedhatsalem@gmail.com"
app_license = "unlicense"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ap_modules/css/ap_modules.css"
# app_include_js = "/assets/ap_modules/js/ap_modules.js"

# include js, css files in header of web template
# web_include_css = "/assets/ap_modules/css/ap_modules.css"
# web_include_js = "/assets/ap_modules/js/ap_modules.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ap_modules/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ap_modules/public/icons.svg"

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
# 	"methods": "ap_modules.utils.jinja_methods",
# 	"filters": "ap_modules.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ap_modules.install.before_install"
# after_install = "ap_modules.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ap_modules.uninstall.before_uninstall"
# after_uninstall = "ap_modules.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ap_modules.utils.before_app_install"
# after_app_install = "ap_modules.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ap_modules.utils.before_app_uninstall"
# after_app_uninstall = "ap_modules.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ap_modules.notifications.get_notification_config"

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

override_doctype_class = {
    "Server Script": "ap_modules.overrides.server_script.CustomServerScript",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ap_modules.tasks.all"
# 	],
# 	"daily": [
# 		"ap_modules.tasks.daily"
# 	],
# 	"hourly": [
# 		"ap_modules.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ap_modules.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ap_modules.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ap_modules.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ap_modules.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ap_modules.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ap_modules.utils.before_request"]
# after_request = ["ap_modules.utils.after_request"]

# Job Events
# ----------
# before_job = ["ap_modules.utils.before_job"]
# after_job = ["ap_modules.utils.after_job"]

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
# 	"ap_modules.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

