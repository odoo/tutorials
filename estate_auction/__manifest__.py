# -*- coding: utf-8 -*-

{
    'name': 'Real Estate Auction',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Automated auction system for real estate properties',
    'author': 'Maan Patel',
    'depends': ['estate', 'mail', 'estate_account'],
    'description': """
        This module extends the real estate module by adding an automated
        auction system where users can bid on properties. The auction process
        includes automatic winner selection, highest bid tracking, and email
        notifications for participants.
    """,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_offer_form.xml',
        'views/estate_properties_template.xml',
        'views/estate_properties_details.xml',
        'data/ir_cron_data.xml'
    ],
        'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/auction_status_selection.js',
            'estate_auction/static/src/components/auction_state_selection/auction_status_selection_form.js',
            'estate_auction/static/src/components/auction_state_selection/auction_status_selection_form.xml',
            'estate_auction/static/src/components/auction_state_selection/auction_status_selection.scss'
        ]
    },
    'license': 'LGPL-3',
    'installable': True
}
