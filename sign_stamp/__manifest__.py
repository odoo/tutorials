{
    'name': "Sign Stamp",
    'version': '1.0',
    'category': 'Sales/Sign',
    'description': """
        Apply Stamp on any document
    """,
    'depends': ['sign'],
    'author': "Soham Zadafiya [soza]",
    'data': [
        'data/sign_data.xml',
        'data/stamp_tour.xml',
        'views/sign_request_templates.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OEEL-1',
    'assets': {
        'web.assets_backend': [
            'sign_stamp/static/src/backend_components/**/*',
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/**/*',
            'sign_stamp/static/src/js/tours/**/*',
        ],
        'web.qunit_suite_tests': [
            'sign_stamp/static/tests/**/*',
        ],
        'sign.assets_public_sign': [
            'sign_stamp/static/src/components/**/*',
            'sign_stamp/static/src/dialogs/**/*',
        ]
    }
}
