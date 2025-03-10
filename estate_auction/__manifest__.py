{
  'name' : "Estate Auction",
  'version' : '1.0',
  'depends' : ['base', 'estate'],
  'category' : 'RealEstate/Auction',
  'author' : "BHPR",
  'description' : "A real estate app with auction functionality.",
  'data' : [
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_website_inherit_templates.xml',
        'data/scheduled_actions.xml',
        'data/email_template.xml'
   ],
   'assets' : {
          'web.assets_backend': [
            'estate_auction/static/src/components/auction_state_selection/**/*',
        ],
          'web.assets_frontend': [
            'estate_auction/static/src/timer_widgets/**/*.js',
        ]
   },
   'license' : 'LGPL-3',
   'auto_install' : True,
   'application' : True,
}
