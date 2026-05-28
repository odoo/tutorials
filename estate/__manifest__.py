{
    'name': 'Estate',
    'category': 'Real Estate',
    'sequence': 1,
    'summary': 'Making the real estate app from tutorials',
    'website': 'www.odoo.com',
    'depends': [
        'base', 'mail'
    ],
    'data': [
        'report/ir_actions_report.xml',
        'security/estate_groups.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'wizard/estate_property_offer_view.xml',
        'data/ir_cron_data.xml',
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_visit_view.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Rini Pillai',
    'license': 'LGPL-3',
}
