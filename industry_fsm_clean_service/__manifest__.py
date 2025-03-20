# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Field Service - Cleaning",
    'category': 'Services/Field Service',
    'summary': "Provide trash bin cleaning services on a recurring schedule",
    'description': """
    Automated weekly task generation for field service orders, client notification and optimized route planning
    """,
    'version': "1.0",
    'author': "nees",
    'depends': ['industry_fsm', 'sale_subscription', 'sale_project', 'hr_holidays'],
    'data': [
        'views/res_config_settings_views.xml',
        'data/mail_template_reminder.xml',
        'data/ir_cron_reminder_data.xml',
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend_lazy': [
        'industry_fsm_clean_service/static/src/map_view/map_model.js',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license': "OEEL-1",
}
