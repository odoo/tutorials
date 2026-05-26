{
    'name': 'Real Estate Auction',
    'description': "This module allows creating property auction.",
    'author': 'Sudarshan Maity (sumai)',
    'website': '',
    'category': 'Real Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': [
        'estate',
        ],

    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'data/auction_cron.xml',
        'data/estate_auction_website_template.xml',
        'data/auction_email_templates.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/js/auction_countdown.js',
        ],
    },

    'installable': True,
}
