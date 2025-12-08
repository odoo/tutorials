{
    'name': 'Real Estate Auctions',
    'version': '1.0',
    'depends': ['base', 'estate', 'web'],
    'author': 'Aryan Donga (ardo)',
    'description': 'Real Estate Auctions addon module',
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'views/estate_property_web_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/ir_cron.xml',
        'data/auction_email_templates.xml',
    ],
    'assets': {
        'web.assets_backend': ['estate_auction/static/src/components/**/*'],
        'web.assets_frontend': ['estate_auction/static/src/js/countdown_timer.js'],
    },
}
