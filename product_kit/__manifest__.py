{
    'name': "Product Kit",
    'version': '1.0',
    'depends': ['base', 'sale_management'],
    'author': "Hitesh Prajapati",
    'category': 'Product/Product Kit',
    'license': 'LGPL-3',
    'description': """
        Description text
        """,
    'application': True,
    'installable': True,
     'data':[
        'security/ir.model.access.csv',
        'views/product_kit.xml',
        'wizard/product_kit_wizard.xml',
        'report/sale_order_document.xml',
        'report/sale_order_portal_document.xml'
     ]
}
