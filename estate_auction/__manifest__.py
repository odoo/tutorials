{
    'name': 'estate_auction',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Automated Auction System for Real Estate Properties',
    'description': 'This module adds an automated auction system to the Estate module, allowing properties to be auctioned',
    'author': 'Mahavir Patel (pmah)',
    'website': 'https://odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','estate', 'account'],  
    'data': [
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_website_templates.xml",
        "views/estate_property_offer_success_views.xml",
        "views/ir_cron.xml",
        "data/estate_property_offer_mail_template.xml"
    ],
    'assets':{
        'web.assets_frontend': [
            'estate_auction/static/src/js/auction_countdown.js',
        ],
    },
    'installable': True,
}
