{
    'name': "New Product Type",
    'version': "1.0",
    'summary': 'Add kit product type without using BOM',
    'description': """
        This module allows you to sell products as a kit without using 
        the Bill of Materials (BoM) or the Manufacturing module.
    """,
    'depends': ['sale_management'],
    'category': "Inventory",
    'author': "Himilsinh Sindha (hisi)",
    'data': [
        'security/ir.model.access.csv',
        'wizard/kit_subproducts_wizard.xml',
        'report/report_print_subproducts.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
}
