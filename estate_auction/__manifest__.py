{
    'name': 'Estate Auction',
    'version': '1.0',
    'category': 'Real Estate/Auction',
    'description': 'This module adds automated auction for an estate property',
    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/js/auction_timer.js',
        ],
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/*',
        ],
    },
    'depends': ['estate', 'estate_account'],
    'data': [
        'views/estate_property_views.xml',
        'views/properties_list_website_templates.xml',
        'views/properties_auction_website_templates.xml',
        'views/estate_property_offer_views.xml',
        'data/estate_auction_cron.xml',
        'data/email_template.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'license': 'LGPL-3',
}
