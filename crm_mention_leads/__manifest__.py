{
    'name': 'CRM Lead Internet Discovery',
    'category': 'Demo',
    'summary': 'Convert Reddit mentions into CRM leads automatically',
    'description': """
        Scans Reddit for posts matching your product/service keywords,
        scores them for buying intent, and creates leads in CRM automatically.
    """,
    'author': 'ODOO S.A',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_job.xml',
        'views/res_config_settings_views.xml',
        'views/crm_mention_log_views.xml',
        'wizard/mention_setup_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
