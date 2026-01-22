# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Modular Type",
    "summary": "Manage modular types in manufacturing orders and sales orders",
    "description": """
    This module allows you to define and manage modular types for products in the manufacturing process. 
    With this module, you can:
    - Set multiplication factors for manufacturing order components based on sales order lines.
    - Manage different modular types for each product, ensuring flexibility in production processes.
    - Automatically adjust quantities of components based on modular type and the corresponding sales order.
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "version": "1.0",
    "depends": ["base","product","mrp","sale"],
    "license": "LGPL-3",
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/modular_type_wizard_views.xml",
        "views/product_template_views.xml",
        "views/bom_line_views.xml",
        "views/slaes_order_line_views.xml",
        "views/mrp_production_line_views.xml"
    ],
}
