{
    'name': 'Estate Auction',
    'version': '1.0',
    'depends': ['estate', 'base', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_auction_views.xml',
        'views/estate_property_offer_auction_views.xml',
        'views/estate_auction_website_templates.xml',
        'data/auction_bid_result_email_template.xml',
        'data/ir_cron_auction_data.xml',
    ],
    'application': True,
    'author': 'kapat-odoo',
    'license': 'LGPL-3',
}
