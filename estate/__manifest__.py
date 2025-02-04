{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage real estate properties and transactions',
    'category': 'Real Estate',
    'description': """
        This module allows users to manage real estate listings, 
        offers, and transactions efficiently.
    """,
    'author': 'Dev Patel',
    'license': 'LGPL-3',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'application': True,
    'auto_install': False,
}
