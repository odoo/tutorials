{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Rajeev Aanjana',
    'category': 'Real Estate',
    'description': 'A module for managing real estate properties',
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}
