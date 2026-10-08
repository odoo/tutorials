{
    'name': 'Estate',
    'depends': ['base'],
    'author': 'Odoo S.A.',
    'installable': True,
    'application': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.access.csv',
    ],
    'license': 'LGPL-3',
}
