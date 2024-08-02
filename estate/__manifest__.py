{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'sequence': 15,
    'summary': 'Track properties',
    'description': "",
    'installable': True,
    'application': True,
    'depends': ['base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
        ]
}
