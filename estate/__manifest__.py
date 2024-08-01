{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Manage real estate properties',
    'description': 'Module to manage real estate properties',
    'author': 'Akya',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        
    ],
    'installable': True,
    'application': True,
}
