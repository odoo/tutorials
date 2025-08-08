{
    'name': 'Sign Stamp',
    'version': '1.0',
    'depends': ['sign'],
    'data': [
            'data/sign_data.xml',
            'views/sign_request_templates.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OEEL-1',
    'assets': {
        'web.assets_backend': [
                 'sign_stamp/static/src/components/**/*',
                 'sign_stamp/static/src/dialogs/*',
        ],
        'sign.assets_public_sign': [
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/*',
        ]
    },
}
