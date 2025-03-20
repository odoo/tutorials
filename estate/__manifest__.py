{
    "name": "Real Estate",
    "category": "Real Estate",
    "application": True,
    "installable": True,
    "depends":[
        "base",
        "web"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
    ]
}