{
    'name': "Real Estate",
    'depends': ['base'],
    'author': "Odoo",
    'category': 'Category',
    'license': 'LGPL-3',
    'application': True,
    'description': """
    A app for real estate
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}
