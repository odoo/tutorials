{
    'name': 'Real Estate Auction',
    'version': '1.0',
    'category': 'Real Estate',
    'sequence': 15,
    'depends': ['estate', 'estate_account', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_auction_views.xml',
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'views/estate_auction_offer_views.xml',
        'views/estate_auction_template.xml',
        'views/estate_auction_detail_template.xml',
        'views/estate_auction_create_offer_template.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/js/auction_stage.js'
        ],
    },
    'summary': 'Add auction functionality to real estate properties',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
