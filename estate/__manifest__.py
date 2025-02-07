{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Module to manage real estate advertisements',
    'description': 'A module to create and manage real estate advertisements.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
