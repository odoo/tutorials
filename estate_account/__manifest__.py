# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Estate Account",
    "version": "1.0",
    "depends": ["account", "real_estate"],
    "category": "Accounts for Estate",
    "description": """
    This is the link module that helps generating invoices when marking the property as sold.
    """,
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "data": [
        "reports/estate_property_reports.xml",
        "views/estate_property_views.xml",
    ]
}
