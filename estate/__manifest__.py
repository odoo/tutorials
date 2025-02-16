{
    "name": "Real estate",
    "summary": "Create Real Estate leads and close opportunities",
    "depends": ["base","mail"],
    'author': "Priykant Sharma (pssh)",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
    ],
    "demo" : [
        "demo/estate_property_type_demo.xml",
        "demo/estate_property_tag_demo.xml",
        "demo/estate_property_demo.xml",
        "demo/estate_property_offer_demo.xml"
    ],
    "category": "Real Estate/Brokerage",
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
