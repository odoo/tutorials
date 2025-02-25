{
    "name":"product_warranty",
    "version":"1.0",
    "author":"ksni-odoo",
    "depends":["base", "product", "sale_management"],
    "installable": True,
    "license": "LGPL-3",
    "data":[
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/warranty_config_view.xml",
        "views/product_warranty_menus.xml",
        "wizard/product_warranty_wizard_view.xml",
        "views/sale_order_views.xml",
    ]
}
