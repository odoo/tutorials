# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Estate Auction",
    "summary": "Manage auction stages and processes for estate properties",
    "description": """
    This module introduces auction functionality for estate properties in Odoo.
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "version": "1.0",
    "depends": ["base", "estate", "mail","account"],
    "license": "LGPL-3",
    "application": True,
    "data": [
        "views/estate_property_views.xml",
        "views/estate_website_property_views.xml",
        "views/estate_property_offer_success_views.xml",
        "views/estate_auction_property_offer_error.xml",
        "views/ir_cron.xml",
        "data/estate_property_offer_template.xml"
    ],
    'assets':{
        'web.assets_frontend': [
            'estate_auction/static/src/js/countdown.js',
        ],
    }
}
