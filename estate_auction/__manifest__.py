{
    'name': 'Real Estate Auction',
    'description': "Real Estate Auction Management",
    'depends': [
        'estate',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/properties_list_website.xml',
        'views/estate_auction_website_templates.xml',
        'views/estate_property_offer_views.xml',
        'data/update_auction_status_cron.xml',
        'data/mail_templates.xml',
    ],
    'assets': {
        "web.assets_backend": [
            "estate_auction/static/src/components/estate_auction_state_selection/*",
        ],
        "web.assets_frontend": [
            "estate_auction/static/src/js/auction_timer.js",
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
