{
    'name': "Budget",
    'version': '1.0',
    'depends': ['base', 'account'],
    'author': "Hitesh Prajapati",
    'category': 'Budget/Budget',
    'license': 'LGPL-3',
    'application': True,
    'instalable': True,

    'data':[
        'security/ir.model.access.csv',
        'views/account_analytic_line.xml',
        'wizard/budget_wizard.xml',
        'views/budget_budget.xml',
        'views/budget_line.xml',
        'views/budget_menu.xml',
    ]
}
