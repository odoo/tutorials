{
    "name": "Estate Account",
    "category": "Sales",
    "author": "Odoo_In",
    "summary": "use to manage properties account",
    "depends": ["estate", "account"],
    "description": "Manage account",
    "data": [
        'report/estate_account_property_reports.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
