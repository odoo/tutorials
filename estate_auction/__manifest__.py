{
    'name': "Real Estate Auction",
    'version': '1.0',
    'depends': ['estate', 'mail', 'account'],
    'author': "Himilsinh Sindha (hisi)",
    'category': 'Real Estate',
    'description': "Automated Auction for Real Estate Properties",
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'data': [
        'data/ir_cron.xml',
        'data/mail_templates.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_website_templates.xml',
        'views/estate_website_pages_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/**/*',
        ],
        'web.assets_frontend': [
            'estate_auction/static/src/js/**/*.js',
        ]
    },
}
