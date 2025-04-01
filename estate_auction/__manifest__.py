{
    'name': "Estate Auction",
    'version': '1.0',
    'depends': ['base','real_estate','website'],
    'author': "Rishav Shah (sris)",
    'category': 'Estate Auction',
    'icon':'/estate_account/static/src/img/auction_icon.png',
    'description': """    
        Estate Auction module used for enabling auction feature
      """,
    'installable':True,
    'application':True,
    'license':'LGPL-3',
    'data': [
      'views/estate_auction_property_offer_views.xml',
      'views/estate_auction_property_views.xml',
      'views/auction_website_property_template.xml',
    ],
}
