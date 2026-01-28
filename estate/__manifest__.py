{
    'name': 'Real Estate',
    'version': '1.9',
    'category': 'Real Estates',
    'summary': 'Manage real estate operations',
    'author': 'Haroune Hassine',
    'license': 'LGPL-3',
    'depends': [
        'base_setup',
    ],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
}
