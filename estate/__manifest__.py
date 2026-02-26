{
    'name': 'Estate',
    'author': 'Sébastien Laurent',
    "license": 'LGPL-3',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
        'data/estate.property.type.csv',
        ],
    'demo': [
        'demo/estate.property.xml',
        'demo/estate.property.offer.xml',
    ],
}
