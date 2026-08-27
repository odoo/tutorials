# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "estate",
    "application": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_offer_views.xml",
        "views/estate_type_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_menus.xml",
        "views/res_user.xml",
    ],
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
