{
    'name': 'Budget Management CHKH',
    'category': 'Accounting/Accounting',
    'icon': '/budget_management/static/description/icon.png',
    'depends': ['base','mail','analytic','accountant'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/budget_split_wizard_view.xml',
        'views/budget_line_views.xml',
        "views/account_analytical_line_views.xml",
        'views/budget_views.xml',
        'views/budget_menus.xml'
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}
