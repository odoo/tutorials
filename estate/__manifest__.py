{
    'name': 'ESTATE',
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
