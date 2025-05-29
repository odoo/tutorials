{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base', 'sale', 'mail'],
    'author': 'Rajeev Aanjana',
    'category': 'Real Estate',
    'description': 'A module for managing real estate properties',
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}


