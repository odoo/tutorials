{
    'name': "Real Estate",
    'depends': ['base', 'mail', 'website'],
    'author': "Ayush Kumar Singh",
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml', 
        'views/estate_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_offers_demo.xml',
    ],
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3'                                   # default LGPL-3 but if not specified then we get warning in terminal 
}
