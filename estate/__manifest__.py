{
    'name': "Real Estate",
    'license': 'LGPL-3',
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo S.A.",
    'category': 'Category',
    'description': """
    Real Estate Advertisement module
    """,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
