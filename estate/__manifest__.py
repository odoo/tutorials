
{
    'name': 'Real Estate',
    'depends': [
        'base'
    ],
    'category': 'Tutorials',
    'application': True,
    'installable': True,

    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml'
    ]
}