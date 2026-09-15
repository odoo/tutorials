{
    'name': 'Real Estate',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
    ],
    'application': True,
}
