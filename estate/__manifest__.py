{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': [
        'base',
    ],
    'data': [
        'views/estate_property_views.xml',
        'data/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'demo': ['demo/demo_data.xml']
}
