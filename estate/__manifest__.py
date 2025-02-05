{
    'name': 'Estate',
    'version':'1.0',
    'depends': ['base'],
    'description': """This is a base version of the Estate module for real estate management.""",
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
    ],
    'application': True,
    'installable':True,
    # 'auto_install': False,
}
