{
    'name': "Sale Product Kit",
    'description': """
        This custom module add a function to odoo to sell products as a kit, but not using a BOM or the manufacturing module
    """,
    'author': "Dhruv Godhani",
    'installable': True,
    'depends': ['sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "wizard/product_sub_wizard_views.xml",
        "report/sale_order_invoice_report.xml",
        "report/sale_order_portal_report.xml",
        "report/sale_order_report.xml",
    ],
    'license': 'LGPL-3',
    'category': 'Sales',
}
