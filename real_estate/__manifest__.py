{
    'name': "Real Estate",
    'summary': "Starting module for Real Estate Project",
    'description': "Starting module for Real Estate Project Description",
    'category': 'Tutorials',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menu_views.xml'
    ],
    'license': 'AGPL-3'
}
