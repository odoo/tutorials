{
    'name': 'Timesheet Kiosk',
    'version': '1.0',
    'author': 'Parth Sawant',
    'license': 'LGPL-3',
    'summary': 'Timesheet Kiosk for recording employee hours',
    'description': """
        Kiosk application for employees to log timesheet
        entries without needing Odoo backend access.
    """,
    'depends': [
        'hr_timesheet',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'data/mail_template_data.xml',
        'views/res_config_settings_views.xml',
        'views/project_task_views.xml',
        'views/timesheet_kiosk_menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'timesheet_kiosk/static/src/timesheetkiosk/kiosk_app.js',
            'timesheet_kiosk/static/src/timesheetkiosk/kiosk_app.xml',
            'timesheet_kiosk/static/src/timesheetkiosk/kiosk_app.scss',
            'timesheet_kiosk/static/src/timesheetkiosk/start_screen/start_screen.js',
            'timesheet_kiosk/static/src/timesheetkiosk/start_screen/start_screen.xml',
            'timesheet_kiosk/static/src/timesheetkiosk/task_screen/task_screen.js',
            'timesheet_kiosk/static/src/timesheetkiosk/task_screen/task_screen.xml',
            'timesheet_kiosk/static/src/timesheetkiosk/task_screen2/task_screen2.js',
            'timesheet_kiosk/static/src/timesheetkiosk/task_screen2/task_screen2.xml',
        ],
    },

    'application': True,
}