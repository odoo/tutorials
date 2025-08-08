{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'depends': ['mail', 'website'],
    'author': 'Odoo - Rushil Patel',
    'description': 'Technical training (Server Framework)',
    'license': 'LGPL-3',
    'data': [
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_menus.xml',
        'views/res_users_views.xml',
        'views/estate_property_template.xml',
        'report/estate_property_report_templates.xml',
        'report/estate_property_report_views.xml',
    ],
    'demo' : [
        'data/estate_property_demo.xml'
    ],
    'application': True
}
