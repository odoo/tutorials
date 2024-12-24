{
    "name": "Real Estate",
    "author": "Odoo",
    "website": "https://www.odoo.com/page/realestate",
    "version": "0.1",
    "application": True,
    "installable": True,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/estate_res_user_views.xml",
    ],
    "license": "LGPL-3",
}
