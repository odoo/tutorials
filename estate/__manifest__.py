{
    'name': "Real estate",
    'version': "1.0.0",
    'depends': ["base", "web","mail"],
    'author': "Mehul Kotak",
    'category': "Tutorials",
    'description': "This Real Estate app in which the ad for any propertiues can add and also buyer can see and give thier price for that property",
    'application': True,
    'installable': True,
    'license': "LGPL-3",
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_menus.xml",
    ],
}
