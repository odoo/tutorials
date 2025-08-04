{
    'name': 'Estate',
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'application': True,
    'installable': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_user_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'license': 'LGPL-3',
}
