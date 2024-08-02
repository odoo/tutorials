{
    'name': 'estate',
    'version': '1.0',
    'summary': 'Real Estate Advertisement Module',
    'description': 'A module for managing real estate advertisements.',
    'category': 'Sales',
    'author': 'YASP',
    'website': 'http://www.estatedemo.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
