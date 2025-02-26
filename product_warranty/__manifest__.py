{
    'name': "product_warranty",
    'category': "Sales/Sales",
    'license': "AGPL-3",
    'version': "1.0",
    'depends': ["sale_management"],
    'data': [
        "wizard/product_warranty_wizard.xml",
        "views/product_warranty_view.xml",
        "views/product_warranty_menu.xml",
        "views/sale_order_product_warranty.xml",
        "views/sale_order_add_warranty.xml",
        "security/ir.model.access.csv"
    ],
    'installable': True,
    'application': True
}
