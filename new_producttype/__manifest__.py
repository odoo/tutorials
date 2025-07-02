{
    'name': "New Product Type",
    'category': '',
    'version': '0.1',
    'depends': ['sale'],
    'sequence': 1,
    'application': True,
    'installable': True,
    'data': [
        "security/ir.model.access.csv",
        "report/sub_product_report.xml",
        "wizard/sub_product_kit_wizard_view.xml",
        "views/product_views.xml",
        "views/sale_order_view.xml",
        "views/sub_product_customer_preview.xml",
    ],
    'license': 'AGPL-3'
}
