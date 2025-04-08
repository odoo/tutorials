{
    'name': 'Send Invoice By Email',
    'version': '1.0',
    'summary': 'automated action to send invoice by email',
    'author': 'chirag Gami(chga)',
    'category': 'Invoice',
    'depends': ['base', 'account'],
    'license': 'LGPL-3',
    'data': [
        'views/res_config_settings_views.xml',
        'views/ir_cron_send_email.xml',
    ],
    'installable': True,
    'application': True,
}
