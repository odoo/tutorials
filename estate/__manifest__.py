{
    'name': 'Estate',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
    ],
    'application': True,
    'installable': True,
    'author': 'macou',
    'license': 'LGPL-3',
}
