{
    'name': 'estate',
    'depends': [
        'base',
    ],
    'application': 'True',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
}
