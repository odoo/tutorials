{
    'name': 'Real Estate',
    'description': "Real Estate Advertisement",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    'license': 'AGPL-3'
}
