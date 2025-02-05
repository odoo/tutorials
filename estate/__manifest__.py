{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv', 
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_menus.xml',

    ],
    'installable': True,
    'application': True,
}

