{
    'name': 'Property Kit',
    'version': '0.1',
    'summary': 'this will allow user to sell product as a kit',
    'description': """
Introduces a new 'Kit' product type that allows grouping products without using a Bill of Materials (BoM).
Enables adding sub-products when a product is marked as a kit.
Automatically calculates the kit price based on sub-products.
Provides a user option to control the visibility of sub-products in reports.
    """,
    'author': 'Odoo',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'wizard/kit_add_sub_products_wizard_views.xml',
        'report/sale_order_report_template.xml',
        'views/sale_portal_template.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
