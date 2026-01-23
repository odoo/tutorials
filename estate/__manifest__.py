# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Estate",
    "depends": ["base"],
    "data": [
        "data/ir.model.access.csv",
        "views/estate_list_view.xml",
        "views/estate_kanban_view.xml",
        "views/estate_offer_list_view.xml",
        "views/estate_offer_form_view.xml",
        "views/estate_form_view.xml",
        "views/estate_search_view.xml",
        "views/estate_type_view.xml",
        "views/estate_tag_view.xml",
        "views/res_users_view.xml",
        "views/estate_view.xml",
        "views/estate_menu.xml",
    ],
    "installable": True,
    "application": True,
    "author": "Tudor-Calin Panzaru (tupan)",
    "license": "LGPL-3",
}
