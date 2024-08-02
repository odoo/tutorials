{
    'name': 'estate',
    'version': '1.0',
    'summary': 'This is E-state module about the property',
    'description': 'A detailed description of my module',
    'category': 'Sales',
    'author': 'pkgu',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
