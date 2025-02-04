{
    'name': 'Estate',
    'description': "Real Estate Management",
    'depends': ['base'],
    'author': "sbbh",
    'category': 'Real Estate/Brokerage',
    'data': [
        'security/ir.model.access.csv',  # access rights file
        'views/estate_property_views.xml', 
        'views/estate_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}