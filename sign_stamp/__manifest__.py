{
    'author': 'Odoo S.A.',
    'name': 'Sign Stamp',
    'description': """
    add stamp field in sing app
    """,
    'data': [
        'data/sign_data.xml',
        'views/sign_request_templates.xml'
    ],
    'depends': ['sign'],
    'license': 'LGPL-3',
    'application': True,
    'installable': True
}
