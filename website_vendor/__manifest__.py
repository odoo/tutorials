{
    'name': "Vendor Portal",
    'summary': "A portal for vendors to compare products and create purchase orders.",
    'description': """
        This module provides a vendor portal where users can compare different vendors, 
        view their products, and create purchase orders directly from the website.
    """,
    'version': '1.0',
    'category': 'Purchase',
    'application': True,
    'installable': True,
    'depends': ['purchase', 'website'],
    'data': [
        "security/website_vendor.xml",
        
        "views/products_views.xml",
        "views/purchase_order_dialog.xml",
        "views/purchase_order_templates.xml",
        
        "views/website_template.xml",
        "views/website_vendor_templates.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'website_vendor/static/src/purchase_order_dialog.js',
        ],
    },
    'license': 'AGPL-3'
}
