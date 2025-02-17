{
    'name': 'Real Estate',
    'description': "Real Estate Management",
    'depends': [
        'base',
        'mail'
    ],
    'author': "sbbh",
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'report/estate_reports.xml',
        'report/estate_report_templates.xml'
    ],
    'demo': [
        'demo/estate_property_data.xml',
        'demo/estate_property_offer_data.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
