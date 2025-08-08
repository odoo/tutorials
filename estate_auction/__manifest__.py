{
    'name': 'Estate Auction',
    'version': '1.0',
    'depends': ['estate'],
    'author': 'matd',
    'category': 'Category',
    'description': """
It provides real estate auction module
""",
    'data': [
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'views/property_website_template.xml',
        'views/property_website_detail_template.xml',
        'views/property_website_offer_form_template.xml',
        'views/estate_property_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/auction_countdown/**/*.js'
        ],
        'web.assets_backend': [
            'estate_auction/static/src/auction_state_selection/**/*',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
