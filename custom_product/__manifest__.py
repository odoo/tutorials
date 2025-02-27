{
    'name':'custom_product',
    'author':'dijo',
    'version':'1.2',
    'summary':'This is product module developed by deep i. joshi',
    'category': 'Sales/Sales',
    'license': 'LGPL-3',
    'application': True,
    'depends': ['product','sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "views/kit_wizard_button.xml",
        "wizard/kit_wizard.xml",
        "views/product_template_views.xml"
    ]
}
