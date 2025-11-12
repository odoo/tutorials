{
    'name':'auction_real_estate',
    'version':'1.0',
    'author':'assh-odoo',
    'depends':['estate', 'estate_account'],
    'data':[
        'views/estate_property_offer_views.xml',
        'views/estate_account_invoice.xml',
        'views/estate_property_views.xml',
        'data/service_cron.xml',
        'views/estate_property_template.xml',
        'views/estate_property_offer_template.xml',
        'views/estate_property_email_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'auction_real_estate/static/src/js/auction_timer.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3'
}
