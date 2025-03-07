{
    'name': 'Real Estate Auction',
    'summary': 'Adds Auction option the properties',
    'author': 'Sudhirkumar Sharma',
    'website': 'https://www.odoo.com',
    'depends':['estate'],
    'data':[
        'data/cron_job.xml',
        'data/mail_template.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_template.xml',
    ],
    'assets':{
        'web.assets_frontend':[
            'estate_auction/static/src/countdown_timer/counter_timer.js',
        ],
    },
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
