{
    'name': 'estate',
    'version': '1.0',
    'summary': 'An real state management application',
    'description': 'A detailed description of my module',
    'category': 'Sales',
    'author': 'prgo',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
}
