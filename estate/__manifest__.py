{
    'name': 'Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'Real estate management module',
    'license': 'LGPL-3',
    'description': 'Manage properties, owners, and sales in your real estate agency',
    'category': 'Real Estate',
    'author': 'ksoz',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
}
