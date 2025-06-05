{
    'name': 'Real Estate',
    'category': 'Estate',
    'description': """This module is  sale estate module""",
    'depends': ['base'],
    'data': [
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
    "sequence": 1,
}
