{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
