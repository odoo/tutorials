{
    'name': 'Real Estate',
    'category': 'Real Estate',
    'version': '1.0',
    'author': 'Radhey Detroja(RADET)',
    'license': 'LGPL-3',
    'summary': 'Manage real estate properties',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}
