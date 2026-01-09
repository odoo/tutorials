# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Webshop Product Description",
    "summary": "Add support for extended product descriptions with multilingual capability",
    "description": """
    This module introduces a new field for extended product descriptions, allowing webshop products to have detailed technical information """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "version": "1.0",
    "depends": ["base","website_sale"],
    "license": "LGPL-3",
    "application": True,
    "data": [
        "views/product_views.xml",
        "views/product_website_sale_views.xml",
    ],
}
