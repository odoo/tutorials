{
    'name': 'Estate Auction',
    'version': '1.0',
    'depends': ['estate'],  
    'author': 'Manthan Akbari',
    'license': 'LGPL-3',
    'category': 'Real Estate',
    'summary': 'Adds auction functionality to the estate module',
    'description': 'Manages property auctions, automated bid acceptance, and auction settings.',
    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/timer/display_timer_widgets.js',
        ],
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.js',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.xml',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.scss',
        ],
    },
    'data': [
        'data/cron_job.xml',
        'data/email_template.xml',
        'views/estate_property_views.xml',
        'views/offer_form_template.xml',
        'views/offer_success_template.xml',
        'views/property_listing.xml',
    ],
    'installable': True,
}
