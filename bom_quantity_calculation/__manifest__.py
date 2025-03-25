{
    "name": "BOM quantity canculation",
    "version": "1.0",
    "summary": "computes BOM quantity based on product's parameter",
    "description": """
        This module contains feature for compute BOM quantity, customer schedule date and order of work for reordering rule.
    """,
    "author": "Odoo",
    "depends": ["mrp","sale_management","purchase"],
    'auto_install': True,
    'data': [
        "views/product_template_views.xml",
        "views/mrp_bom_views.xml",
        "views/mrp_production_views.xml",
        "views/purchase_order_views.xml",
        "views/sale_order_views.xml",
    ],
    "license": "LGPL-3",
}
