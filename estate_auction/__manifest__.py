{
    'name': "Estate Auction",
    'version': '1.0',
    'depends': ['base', 'mail', 'real_estate', 'website', 'estate_account', 'project'],
    'author': "Rishav Shah (sris)",
    'category': 'Estate Auction',
    'icon': '/estate_auction/static/src/img/auction_icon.png',
    'description': """
        Estate Auction module used for enabling auction feature
      """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
      'data/ir_cron.xml',
      'data/estate_auction_email_template.xml',
      'views/estate_auction_property_views.xml',
      'views/auction_website_property_template.xml',
    ],
}
