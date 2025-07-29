# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Warranty Management for Products",
    "version": "1.0",
    "category": "Sales",
    "summary": "Manage product warranties",
    "description": """
        This module allows you to manage product warranties, including warranty periods and conditions.
    """,
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_warranty.xml",
        "views/product_warranty_config_views.xml",
        "views/product_warranty_config_menus.xml",
        "views/sale_order_views.xml",
        "wizard/product_warranty_wizard.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
