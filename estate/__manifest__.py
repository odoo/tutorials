{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "pirth",
    'category': 'Tutorial',
    'application': True,
    'installation': True,
    'summary': "Real estate",
    'description': """
    Module about real estate
    """,
    'license': "LGPL-3",
    'data': [
        'security/ir.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}
