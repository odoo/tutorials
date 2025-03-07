{
  'name' : "Estate Auction",
  'version' : '1.0',
  'depends' : ['base', 'estate'],
  'category' : 'RealEstate/Auction',
  'author' : "BHPR",
  'description' : "",
  'data' : [
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_website_inherit_templates.xml',
        'data/scheduled_actions.xml',
        'data/email_template.xml'
   ],
   'assets' : {
     
       'web.assets_backend' : [

            'estate_auction/static/src/components/AuctionStateSelection/**/*',
           
       ]

   },
   'license' : 'LGPL-3',
   'auto_install' : True,
   'application' : True,
}
