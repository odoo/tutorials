{
    'name': 'Revenue Recognition Management',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Automatic revenue recognition for projects with date correction',
    'author': 'Odoo',
    'depends': ['project', 'sale', 'account', 'sale_project'],
    'data': [
        'views/project_revenue_recognition_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
