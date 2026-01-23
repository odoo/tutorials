# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_offer_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_type_views.xml",
        "views/estate_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "application": True,
    "author": "Tudor-Calin Panzaru (tupan)",
    "license": "LGPL-3",
}
