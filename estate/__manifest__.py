{
    'name': 'Estate',
    'depends': [
        'base_setup',
    ],
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'security/ir.access.csv',
        'data/data_estate_property_type.xml',
    ],
    'demo': [
        'demo/demo_estate_property.xml',
        'demo/demo_estate_property_offer.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'viayo',
    'license': 'LGPL-3',
}
