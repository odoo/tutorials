{
    'name': "Product Warranty",
    'version': "1.0",
    'author': "Vaidik Gorasiya - vrgo",
    'depends': ['base', 'sale_management'],
    "data": [
        "security/ir.model.access.csv",
        "data/warranty_data.xml",
        "wizard/add_warranty_wizard.xml",
        "views/product_template_views.xml",
        "views/product_warranty_config_views.xml",
        "views/product_warranty_config_menu.xml",
        "views/sales_order_views.xml",
    ],
    'installable': True,
    'license': 'LGPL-3',
}
