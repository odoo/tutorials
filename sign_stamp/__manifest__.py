{
    'author': 'Odoo S.A.',
    'name': 'Sign Stamp',
    'description': """
    add stamp field in sing app
    """,
    'depends': ['sign', 'web'],
    'data': [
        'data/sign_data.xml',
        'views/sign_request_templates.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/**/*',
        ],
        'web.assets_frontend': [
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/**/*',
        ],
        'sign.assets_public_sign': [
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/**/*',
        ],
    },
    'license': 'LGPL-3',
    'application': True,
    'installable': True
}
