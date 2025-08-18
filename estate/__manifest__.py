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
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ],
    'license': 'LGPL-3',
}
