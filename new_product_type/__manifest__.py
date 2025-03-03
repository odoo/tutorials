{
    'name': 'Product Kit Type for Product',
    'version': '1.0',
    'summary': 'Sell products as kits without BoM or Manufacturing Module',
    'description': """
        This module allows selling products as kits, grouping sub-products under a main product in the Sales module.
    """,
    'author': 'Mandani Tushar',
    'depends': ['sale_management'],
    'data': ['security/ir.model.access.csv',
            'report/sale_order_report.xml',
            'views/sale_order_customer_preview.xml',
            'views/product_view.xml',
            'views/sale_order_form_views.xml',
            'wizard/sub_product_wizard_views.xml'
    ],
    'license': 'LGPL-3'   
}
