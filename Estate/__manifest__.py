{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Vansh",
    'category': 'estate',
    'description': """Find Your property Here""",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'application': True,
    'installable': True,
    'license': "AGPL-3"
}
