{
    "name": "Warranty Configuration",
    "version": "1.0",
    "depends": ["base", "sale_management", "spreadsheet"],
    "author": "djip-odoo",
    "description": """
        Part of technical training
        Creating Warranty Configuration module for assignment 1
    """,
    "data": [
        "security/ir.model.access.csv",
        "wizards/add_warranty_wizard_view.xml",
        "views/sales_management_menu.xml",
        "views/warranty_configuration_views.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml",
    ],
    'demo':[        
        'demo/product_demo.xml',
        'demo/warranty_configuration_demo.xml',
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
