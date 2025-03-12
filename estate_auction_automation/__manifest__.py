{
    'name': "Real Estate Auction",
    'version': '1.0',
    'depends': ['estate', 'estate_account','account'],
    'category': 'Real Estate/Brokerage',
    'description': """
    The Real Estate Auction Automation
    """,
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
    
    "data": [
        "data/ir_cron.xml",
        "data/estate_property_offer_mail_template.xml",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_website_template.xml",
    ],
   
    'assets': {
        'web.assets_backend': [
            'estate_auction_automation/static/src/**/*',
             ('remove', 'estate_auction_automation/static/src/js/**/*'),
        ],
        'web.assets_frontend': [
            'estate_auction_automation/static/src/js/**/*',
        ]
    },
}
