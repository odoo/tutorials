{
    'name': 'Budget Management',
    'description': 'A Sample Budget Management Module',
    'version': '1.0',
    
    'depends': ['base', 'analytic'],
    'category': 'Accounting/Budget',
    
    'application': True,
    'installable': True,
    
    'author': 'Kishan B. Gajera',
    
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'wizard/create_multiple_budgets_views.xml',
        'views/budget_budget_views.xml',
        'views/budget_budget_lines_views.xml',
        'views/analytic_line_views.xml',
    ],
    'demo': [],
}
