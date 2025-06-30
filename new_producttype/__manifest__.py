{
    'name': "New Product Type",
    'category': '',
    'version': '0.1',
    'depends': ['sale'],
    'sequence': 1,
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        "wizard/sub_product_kit_wizard_view.xml",
        "views/product_views.xml",
        "views/sale_order_view.xml",
    ],
    'license': 'AGPL-3'
}
