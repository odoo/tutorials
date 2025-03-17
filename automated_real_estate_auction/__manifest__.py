# -*- coding: utf-8 -*-

{
    "name": "Automated Real Estate Auction",
    "category": "Real Estate/Brokerage",
    "depends":["estate","estate_account",'mail'],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_properties_details.xml',
        'views/estate_properties_template.xml',
        'views/check_auction_complete.xml',
        'views/congratulations_page.xml',
        'views/add_offer_page.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'automated_real_estate_auction/static/src/components/auction_state_selection/status_of_property.scss',
            'automated_real_estate_auction/static/src/components/auction_state_selection/auction_status_selection_form.xml',
            'automated_real_estate_auction/static/src/components/auction_state_selection/status_of_property_kanban.js',
            'automated_real_estate_auction/static/src/components/auction_state_selection/status_of_property_form.js',
        ],
    },
    'installable': True,
    "license": "LGPL-3"
}
