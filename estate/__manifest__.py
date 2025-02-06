{
    'name': 'Real Estate',
    'version': '1.0',
    'sequence' : 1,
    'depends': ['base'],
    'author': 'matd',
    'category': 'Category',
    'description': """
    It provides real estate module
    """,
    'data': [
        'security/ir.model.access.csv',

        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    'application': True,
}
