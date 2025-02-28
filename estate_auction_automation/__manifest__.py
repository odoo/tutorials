{
    'name': "Real Estate Auction",
    'version': '1.0',
    'depends': ['estate', 'estate_account', 'web'],
    'author': "Prince Beladiya",
    'category': 'Real Estate/Brokerage',
    'icon': '/estate_auction_automation/static/img/icon.png',
    'description': """
    The Real Estate Auction AUtomation
    """,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'data/ir_cron.xml',
        'data/mail_templates.xml',
        'views/account_move_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'estate_auction_automation/static/src/**/*'
        ]
    }
}
