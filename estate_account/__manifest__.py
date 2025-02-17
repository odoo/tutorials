# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.  

{
    "name": "Real Estate Accounting",
    "depends": ["estate", "account"],
    "category": "Accounting",
    "license": "LGPL-3",
    "description": "Links the Estate module with Accounting for automatic invoice creation.",
    "data": ['report/estate_property_reports.xml'],
    "installable": True,
    "application": True,
}
