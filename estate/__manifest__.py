{
    'name': 'Real Estate',
    'author': 'Aditi (adpaw)',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
}
