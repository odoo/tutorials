{
    "name": "Automated Real Estate Auction",
    "version": "1.0",
    "depends": ["base", "estate", "mail"],
    "description": "Automate auction process to reduce delays",
    "data": [
        "security/ir.model.access.csv",
        "data/estate_property_mail_template.xml",
        "views/estate_property_offer_placed_views.xml",
        "views/estate_property_make_offer_views.xml",
        "views/estate_property_detail_website.xml",
        "views/estate_property_list_website.xml",
        "views/estate_property_views.xml",
        "data/ir_cron.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "automated_estate_auction/static/src/js/auction_countdown.js"
        ],
        "web.assets_backend": [
            "automated_estate_auction/static/src/component/auction_state_widget.js",
            "automated_estate_auction/static/src/component/auction_state_widget.scss",
            "automated_estate_auction/static/src/component/auction_state_widget.xml",
        ],
    },
    "sequence": 1,
    "application": True,
    "license": "OEEL-1",
    "installable": True,
}
