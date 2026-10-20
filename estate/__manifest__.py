{
    'name': 'My Real Estate',
    'author': 'Odoo S.A.',
    'category': 'Tutorials',
    'installable': True,
    'application': True,
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
