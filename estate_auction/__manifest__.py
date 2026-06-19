{
    'name': 'RealEstateAuction',
    'version': '1.0',
    'depends': ['estate', 'web'],
    'author': 'Pranjali Sangavekar(prsan)',
    'license': 'LGPL-3',
    'application': True,

    'data': [
        'views/estate_auction_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.js',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.xml',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.scss',
        ],
    },
}