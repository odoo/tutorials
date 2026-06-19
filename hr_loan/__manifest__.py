{
    'name': 'Employee Loan',
    'version': '1.0',
    'category': 'Tutorials',
    'Summary': 'Employee Loan System',
    'description': 'Manage your Loans',
    'application': True,
    'installable': True,
    'author': 'times',
    'website': 'https://www.odoo.com/app/loan',
    'depends': [
        'base',
        'hr',
        'hr_payroll'
    ],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'security/hr_loan_security.xml',
        'data/hr_loan_salary_rule.xml',
        'views/hr_loan_views.xml',
        'views/hr_menus.xml',
    ],
}
