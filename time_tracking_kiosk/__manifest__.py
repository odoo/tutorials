# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Timesheet Kiosk",
    "version": "1.0",
    "summary": "Record working hours from kiosk mode for projects and tasks",
    "category": "Tutorials",
    "description": """
        This module allows employees to record their working hours via a kiosk interface:
        - Scan employee badge to identify user
        - Select projects and tasks assigned to the employee
        - Start/stop timers to track work accurately
        - Configure maximum allowed hours and minimum time entries
        - Allow portal users access to timesheets
        - Notify project managers via configurable email templates
    """,
    "author": "nmak",
    "depends": ["base", "hr_timesheet", "project", "hr_attendance"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir.rule.xml",
        "data/email_template.xml",
        "views/timesheet_kiosk_actions.xml",
        "views/hr_employee_form_views.xml",
        "views/res_config_settings_view.xml",
        "views/timesheet_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "time_tracking_kiosk/static/src/kiosk_main.js",
            "time_tracking_kiosk/static/src/scss/style.scss",
            "time_tracking_kiosk/static/src/timesheet_kiosk_templates.xml",
        ],
    },
    "application": True,
    'post_init_hook': 'set_menu_visibility_for_kiosk',
    "installable": True,
    "license": "LGPL-3",
}
