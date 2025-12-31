{
    'author': 'Odoo S.A.',
    'name': 'Sign Stamp',
    'description': """
    Adds a Company Stamp feature to the Sign application.
    This module introduces a new Stamp sign item that allows companies to
    apply an official stamp containing company details such as name, address,
    VAT number, and logo. The stamp is rendered dynamically and can be used
    as a valid electronic signature when signing documents.
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
