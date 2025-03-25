# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Real Estate Accounting",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Create real estate invoices!",
    "category": "Tutorials/RealEstate",
    "depends": ["estate", "account"],
    "data": [
        "reports/estate_property_templates.xml",
        "views/estate_property_views.xml"
    ],
    "installable": True,
    "license": "LGPL-3"
}
