# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate Auctions",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Automate real estate auctions!",
    "category": "Tutorials/RealEstate",
    "depends": ["estate"],
    "data": [
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "views/estate_property_views.xml",
        "views/estate_property_templates.xml"
    ],
    "installable": True,
    "license": "LGPL-3"
}
