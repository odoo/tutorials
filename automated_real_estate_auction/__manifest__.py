{
    'name' : "Automated Real Estate Auction",
    'version' : '1.0',
    'category' : 'Real Estate',
    'summary' : 'Module to set automated auction for real estate module',
    'depends' : ['estate', 'estate_account'],
    'data' : [
        'data/cron.xml',
        'views/estate_property_views.xml',
        'views/estate_property_auction_template.xml',
    ],
    'assets': {
       'web.assets_frontend': [
          'automated_real_estate_auction/static/src/js/**/*',
       ],
       'web.assets_backend': [
           'automated_real_estate_auction/static/src/components/**/*'
        ],
    },
    'installable' : True,
    'license': 'AGPL-3',
}
