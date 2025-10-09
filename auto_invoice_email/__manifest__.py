{
    'name': 'Automatic Invoice Email',
    'summary': 'Automatically send posted invoices by email after X days',
    'depends': ['account', 'mail'],
    'data': [
        'data/cron.xml',
        'views/res_config_settings_views.xml',
    ],
    "license": "LGPL-3",
    'installable': True,
}
