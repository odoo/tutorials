{
    'name': 'Real Estate Auction',
    'summary': 'Adds Auction option the properties',
    'author': 'Sudhirkumar Sharma',
    'website': 'https://www.odoo.com',
    'depends':['estate'],
    'data':[
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_template.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'estate_auction/static/src/countdown_timer/counter_timer.js',
            'estate_auction/static/src/countdown_timer/counter_timer.xml',
        ],
    },
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
