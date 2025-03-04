
{
    'name': "Estate Auction",
    'version': "1.0",
    'depends': ["estate"],
    'author': "Prathmesh Soni (pdso)",
    'category': "Tutorials/estate_auction",
    'summary': "A real estate app with auction functionality",
    'description': "A real estate app with auction functionality.",
    'data': [
        'data/ir_cron_job.xml',
        'data/email_template.xml',
        'templates/estate_property_details_templates.xml',
        'templates/estate_property_templates.xml',
        "templates/estate_property_offer_form.xml",
        "templates/estate_property_offer_success.xml",
        "views/estate_property_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'estate_auction/static/src/timer_widgets/display_timer_widgets.js',
        ],
        'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.js',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.xml',
            'estate_auction/static/src/components/auction_state_selection/auction_state_selection.scss',
        ]
    },
    'sequence': 1,
    'application': True,
    'installable': True,
    'maintainer': "Prathmesh Soni (pdso)",
    'license': "LGPL-3",
}
