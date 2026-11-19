{
    'name': "real estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "elsa ringling (elrin)",
    'category': 'Services',
    'description': """
    This is a test module for the server framework 101 tutorial
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
