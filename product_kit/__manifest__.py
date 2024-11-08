{
    'name': 'Kit Product Sale',
    'version': '1.0',
    'category': 'Sales',
    'author': 'rame_odoo',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/add_sub_product_wizard_view.xml',
        'views/inherited_product_template_view.xml',
        'views/inherited_sale_order_form_view.xml',
        'reports/report_saleorder_subproducts.xml'
    ],
    'installable': True,
    'application': False,
}
