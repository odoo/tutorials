{
    'name': "Real Estate - Auction",
    'version': '1.0',
    'depends': ['estate_account'],
    'author': "Vaidik Gorasiya - vrgo",
    'description': """
        This module is designed to manage auction for real estate properties.
    """,
    'category': 'Real Estate',
    'data': [
        'views/account_invoice_views.xml',
        'views/estate_property_views.xml',
        'data/ir_cron.xml',
        'views/estate_website.xml',
        'data/mail_template_data.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/**/*'
        ],
        'web.assets_frontend': [
            'estate_auction/static/src/js/**/*'
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
