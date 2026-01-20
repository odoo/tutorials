{
    'name' : "Real Estate Auction",
    'summary' : "A module adding auction functionality to real estate management in Odoo.",
    'author': "krge",
    'website': "https://www.odoo.com",
    'category': 'Tutorials',
    'version': '0.1',
    'depends': ['estate'],
    'installable': True,
    'data': [
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_templete.xml',
        'data/property_offer_email.xml',
        'data/ir_cron_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate_auction/static/src/components/**/*',
        ],
        'web.assets_frontend': [
            'estate_auction/static/src/js/**/*',
        ],
    },
    'license': 'AGPL-3'
}
