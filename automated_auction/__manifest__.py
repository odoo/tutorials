{
    'name': "Automated Auction",
    'version': '1.0',
    'depends': ['estate'],
    'author': "ppch",
    'category': '',
    'description': """
    Automated Auction module for Estate properties
    """,
    'license': "LGPL-3",
    'data': [
        'data/service_cron.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/property_add_offer_template.xml',
        'views/property_templates.xml',
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_frontend': [
            'automated_auction/static/src/timer.js',
        ],
        'web.assets_backend': [
            'automated_auction/static/src/auction_state_widget/**/*.js',
            'automated_auction/static/src/auction_state_widget/**/*.xml',
            'automated_auction/static/src/auction_state_widget/**/*.scss',
        ],
    },
    'installable': True,
}
