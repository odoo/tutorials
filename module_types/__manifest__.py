{
    'name': 'Product Module type',
    'version': '1.0',
    'category': 'Sales/Manufacturing',
    'summary': 'Enable Modular types feature for Manufacturing orders',
    'depends': ['sale_mrp', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_module_types_wizard.xml',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'views/sales_order_views.xml',
        'views/stock_move_views.xml'
    ],
    'installable': True,
    'license': 'LGPL-3'
}
