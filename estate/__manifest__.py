# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Real Estate",
    "category":"Real Estate/Brokerage",
    "license": "LGPL-3",
    "version" : "1.0",
    "depends": [
        "base"
    ],
    "data": [
         "security/security.xml",
         "security/ir.model.access.csv",
         "views/estate_property_tag.xml",
         "views/estate_property_offer_action.xml",
         "views/estate_property_type_action.xml",
         "views/estate_property_view.xml",
         "views/res_users_inherit.xml",
         "views/estate_menu.xml",
         "data/master_data.xml",
         "report/estate_reports.xml",
         "report/estate_reports_views.xml"
    ],
    "demo": [
        "demo/demo_data.xml"
    ],
    "installable": True,
    "application": True,
}
