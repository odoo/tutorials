{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_menus.xml",
        "security/ir.model.access.csv"
    ]
}
