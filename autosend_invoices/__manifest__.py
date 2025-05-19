# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Auto Send Invoices",
    'version': '1.0',
    'category': "Hidden",
    'description': """
        Automatically send invoices after specific number of days.
    """,
    'depends': ['account'],
    'data': [
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml'
    ],
    'installable': True,
    'license': "LGPL-3",
}
