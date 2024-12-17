{
    'name': "Real Estate",
    'depends': ['base'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menus.xml"
    ]
}