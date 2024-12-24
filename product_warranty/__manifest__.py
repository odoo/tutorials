{
    'name': 'Product Warranty',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/warranty_config_views.xml",
        "views/warranty_wizard_views.xml",
        "views/sale_order_form_views.xml",
        "views/product_template_views.xml",
        "views/warranty_config_menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install":True,
    "license": "AGPL-3",
    "author": "Odoo",
}
