{
    'name': 'Automatic invoicing',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Configure a schedule to send customer invoices automatically',
    'depends': ['account'],
    'data': [
        'data/ir_cron.xml',
        'views/res_config_settings_views.xml'
    ],
    'installable': True,
    'license': 'LGPL-3'
}
