{
    'name': "Sale Is Kit",
    'category': 'Sales',
    'description': 'Add the kit option',
    'summary': "Create and sell products of type kit",
    'description': """
    This bridge module adds the ability to create and sell products of type kit.
    """,
    'depends': [
        'product',
        'sale',
    ],
    'data': [
        "security/ir.model.access.csv",
        "wizard/sub_product_wizard_views.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "report/sale_order_document_report.xml",
        "views/sale_portal_template.xml"
    ],
        
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}