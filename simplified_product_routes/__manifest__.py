{
    'name': 'Simplified Product Routes',
    'version': '1.0',
    'summary': 'Simplifies route configuration for products',
    'description': """
        This module simplifies route configuration for products by:
        - Automatically applying appropriate routes based on product configuration
        - Merging dropship routes
        - Hiding operation section when no routes are available
    """,
    'website': 'https://www.odoo.com/app/inventory',
    'category': 'Inventory/Inventory',
    'author': 'Himilsinh Sindha (hisi)',
    'depends': ['stock', 'purchase', 'purchase_stock', 'mrp', 'mrp_subcontracting', 'mrp_subcontracting_dropshipping'],
    'data': [
        'views/product_template_views.xml',
        'data/default_route_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
