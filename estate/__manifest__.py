{
    'name': 'estate',
    'version': '1.0',
    'author': 'KAME',
    'depends': ['base', 'mail'],
    'category': 'Real Estate/Brokerage',

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/property_type_data.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_menus.xml',
        'views/res_users_views.xml',
    ],
    'demo': [
        'demo/estate_property_demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3'
}
