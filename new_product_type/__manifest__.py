{
    'name': 'Product Kits for Sales',
    'version': '1.0',
    'summary': 'Sell products as kits without BoM or Manufacturing Module',
    'description': """
        This module allows selling products as kits, grouping sub-products under a main product in the Sales module.
    """,
    'author': 'Mandani Tushar',
    'depends': ['sale', 'product'],
    'data': ['security/ir.model.access.csv',
            'views/product_view.xml',
            'views/sale_order_form_views.xml',
            'wizard/sub_product_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',    
}
