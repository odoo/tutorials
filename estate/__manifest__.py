{
    'name': 'estate',
    'version': '1.0',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',    
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}