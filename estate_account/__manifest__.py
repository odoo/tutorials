{
    "name": "Estate Account",
    "version": "1.0",
    "depends": ["base", "estate", "account"],
    "author": "djip-odoo",
    "description": """
        part of technical training
    """,
    "data": [
        "report/estate_estate_property_templates.xml",
        "security/ir.model.access.csv",
        "views/actions_smart_button.xml",
        "views/estate_property_views.xml",
    ],
    "demo": [
        "demo/demo_invoice_data_property.xml",
    ],
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
