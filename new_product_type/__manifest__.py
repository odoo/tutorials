{
    'name': "New Product Type",
    'version': "1.0",
    'summary': 'Enhancements for the Product app',
    'description': """
        This module adds custom features to the Sales app for products.
    """,
    'category': "Sales", 
    'author': "BHPR",
    'depends': ['sale','product'], 
    'data': [
         'security/ir.model.access.csv',
         'views/product_template_views.xml',
         'views/sale_order_view.xml',
         'wizard/sub_product_wizard.xml'
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
