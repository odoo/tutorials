{
    'name': 'Product Kit Management',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Odoo S.A.',
    'summary': 'Add a new product type "is_kit" and manage product kits in sales orders.',
    'description': """
        This module introduces a new product type called "Kit" that allows bundling multiple products 
        into a single sale order line. It provides a wizard to manage kit components, updates sales 
        and invoice reports accordingly, and ensures stock and pricing consistency.
    """,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_kit_wizard_view.xml',
        'report/sale_order_report.xml',
        'report/invoice_report.xml',
        'views/sale_product_template.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
