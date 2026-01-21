{
    'name': "Real Estate Auction",
    'version': '1.0',
    'depends': ['estate_account'],
    'category': 'Real Estate/Brokerage',
    'author': "Soham Zadafiya [soza]",
    'description': """
        Autometed Auction For Real Estate
    """,
    'application': True,
    'data' : [
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_website_template.xml',
        'data/auction_cron.xml',
        'data/mail_template_data.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/components/AuctionCountdown/**/*.js'
        ],
        'web.assets_backend': [
            'estate_auction/static/src/components/AuctionStateSelection/**/*',
        ]
    },
    'license': 'LGPL-3'
}
