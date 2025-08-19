{
    'name': 'Send Invoice Email',
    'version': '1.0',
    'summary': 'Automatically send invoices by email after configurable days',
    'author': 'rodh',
    'category': 'Accounting',
     "license": "LGPL-3",
    'depends': [
        'account',
        'base',
    ],
    'data': [
        'views/res_config_settings_view.xml',
        'views/ir_cron_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
