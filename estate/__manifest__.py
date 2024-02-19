{
    'name': 'Real Estate',
    'version': '1.0',
    'description': """
    Real Estate Management
    """,
    'depends': [
        'base',
    ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}
