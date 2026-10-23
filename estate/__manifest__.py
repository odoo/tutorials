{
    'name': 'Estate Agency',
    'author': 'mibar',
    'license': 'LGPL-3',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'security/ir.access.csv',
    ],
}
