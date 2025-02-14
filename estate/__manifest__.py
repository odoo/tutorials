{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Property',
    'sequence': 15,
    'summary': 'Find various properties in a click',
    "depends":['mail'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml',
        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml',
    ]
}
