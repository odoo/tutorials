{
    'name': 'RealEstateAuction',
    'version': '1.0',
    'depends': ['estate', 'web', 'estate_website_settings'],
    'author': 'Pranjali Sangavekar(prsan)',
    'license': 'LGPL-3',
    'application': True,

    'data': [
        'views/estate_auction_view.xml',
        'views/website_property_detail_inherit.xml',
        'data/ir_cron_estate.xml',
        'data/mail_template.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.js',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.xml',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.scss',
        ],

        'web.assets_frontend': [
            'estate_auction/static/src/components/auction_timer/auction_timer.js',
            'estate_auction/static/src/components/auction_timer/auction_timer.xml',
            'estate_auction/static/src/js/main.js',
        ],
    },
}
