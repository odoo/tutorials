{
    'name': "Real Estate - Auction",
    'version': "1.0",
    'depends': ["estate","mail"],
    'category': "Real Estate/Brokerage",
    'data':[
        "data/ir_cron.xml",
        "data/mail_template_data.xml",

        "views/account_invoice_views.xml",
        "views/estate_property_views.xml",
        "views/auction_offer.xml",
        "views/property_details.xml",
        "views/property_listing.xml",
    ],
    'assets': {
        'web.assets_backend': [
            "estate_auction/static/src/components/**/*"
        ],
        'web.assets_frontend': [
            "estate_auction/static/src/js/**/*"
        ],
    },
    'installable': True,
    'license': "LGPL-3",
}
