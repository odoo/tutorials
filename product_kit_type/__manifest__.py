{
    'name': 'Product Type Kit',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Allow selecting salesperson for pos order',
    'depends': ['sale_management'],
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_form_view.xml',
        'views/sale_order_views.xml',
        'views/sale_order_customer_preview.xml',
        'wizard/views/sub_products_view.xml',
        'report/invoice_report.xml'
    ],
    'license': 'LGPL-3',
}
