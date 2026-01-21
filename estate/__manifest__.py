# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Estate",
    "depends": ["base"],
    "data": [
        "data/ir.model.access.csv",
        "views/estate_views.xml",
        "views/estate_list_view.xml",
        "views/estate_offer_list_view.xml",
        "views/estate_offer_form_view.xml",
        "views/estate_form_view.xml",
        "views/estate_search_view.xml",
        "views/estate_type_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_menu.xml",
    ],
    "installable": True,
    "application": True,
}
