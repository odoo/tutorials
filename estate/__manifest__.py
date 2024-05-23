{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mohamed Yousef",
    'category': 'Sales',
    'description': """
    A Real Estate App to ....
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
         'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "LGPL-3"
}