{
    'name': 'Real Estate',
    'author': "Odoo",
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3',
}
