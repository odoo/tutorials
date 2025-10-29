{
    'name': 'Link project date with analytical account',
    'version': '1.0',
    'author': 'Aaryan Parpyani (aarp)',
    'depends': ['sale_project', 'account'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'description': '''
        Changing the project start date will show a button to sync recognition dates
        across invoices and journal entries.
        Ensuring accounting accuracy without manual intervention.
    ''',
    'data': [
        'views/project_project_views.xml',
    ]
}
