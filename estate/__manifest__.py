{
    "name": "Estate",
    "application": True,
    "depends": ["base","mail"],
    "sequence": 1,
    "license": "LGPL-3",
    "installable" : True,
    "data": [
        "security/ir.model.access.csv",

        "views/estate_property_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_offer_views.xml",
        "views/estate_type_views.xml",
        
        "views/estate_menus.xml",
    ],
}
