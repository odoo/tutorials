{
    "name": "Product Warranty Sale",
    "version": "1.0",
    "depends": ["sale_management"],
    'license': 'LGPL-3',
    "category": "Sales",
    "summary": "Add warranty options to sales orders",
    "demo": [
        "demo/warranty_product.xml",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/warranty_config_views.xml",
        "views/add_warranty_wizard_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": True,
}
