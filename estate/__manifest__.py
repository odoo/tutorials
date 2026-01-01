{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['crm'],
    'author': 'jaldip vekariya (javek)',
    'description': """
     An Real Estate App to buy, sell, and rent properties.
     """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}
