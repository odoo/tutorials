{
    'name': 'Budget',
    'version': '1.0',
    'author': 'DhruvKumar Nagar',
    'summary': 'Manage budgets effectively',
    'description': """
        A custom module for creating and managing budgets in Odoo.
    """,
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/budget_line_view.xml',
        'views/budget_menu_view.xml',
        'wizard/budget_wizard_view.xml',
        'views/budget_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "LGPL-3"
}
