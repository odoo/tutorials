{
    'name': 'Real Estate Auction',
    'summary': 'Adds Auction option the properties',
    'author': 'Sudhirkumar Sharma',
    'website': 'https://www.odoo.com',
    'depends':['estate', 'estate_account'],
    'data':[
        'data/cron_job.xml',
        'data/mail_template.xml',
        'views/estate_property_invoice_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_template.xml',
    ],
    'assets':{
        'web.assets_frontend':[
            'estate_auction/static/src/countdown_timer/counter_timer.js',
        ],
        'web.assets_backend':[
            'estate_auction/static/src/auction_state/auction_state.js',
            'estate_auction/static/src/auction_state/auction_state.xml',
            'estate_auction/static/src/auction_state/auction_state.scss',
        ]
    },
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
