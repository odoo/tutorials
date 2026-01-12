{
    'name': "Real Estate",
    'version': "1.0",
    'category': "Real Estate",
    'summary': "Manage real estate properties",
    'description': "This module allows managing properties",
    'depends': ['base'],
    'author': "jakan",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_maintenance_views.xml",
        "views/estate_menus.xml",
    ]
}
