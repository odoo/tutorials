{
    'name': "Kit Kit",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': "Ayushmaan (ayve)",
    'category': "Products Kit",
    'description': """
        FInal Task, Sell Products as a Kit
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/sub_product_wizard_view.xml',
        'views/kit_button_views.xml',
        'report/kit_report_template.xml',
        'views/add_sub_product_button_views.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
}
