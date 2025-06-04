{
    'name': 'Real Estate',
    'category': 'Estate',
    'description': """This module is  sale estate module""",
    'depends': ['base'],
    'data': [
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
