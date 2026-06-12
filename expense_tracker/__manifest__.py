{
    'name': "Expense Tracker",
    'author': "sopat",
    'category': 'Tutorials',
    'version': '0.1',
    'depends': ['base', 'web'],
    'application': True,
    'data': [
        'views/expense_action.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
        'expense_tracker/static/src/js/expense_tracker.js',
        'expense_tracker/static/src/xml/expense_tracker.xml',
    ],
    },
    'license': 'AGPL-3',
}
