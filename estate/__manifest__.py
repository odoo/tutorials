{
    'name': 'Estate',
    'depends': ['base'],
    'author': 'Odoo - Utsav',
    'license': 'LGPL-3',
    'depends':['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'auto_install': False,
}
