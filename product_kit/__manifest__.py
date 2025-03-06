{
    'name': "Product Kit",
    'version': "1.0",
    'description': "ADD PRODUCT KIT FUNCTIONALITY",
    'depends': ["sale_management"],
    'data': [
        "security/ir.model.access.csv",
        "report/ir_actions_report_templates.xml",
        "report/sale_portal_templates.xml",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "wizard/sub_product.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': "LGPL-3"
}
