{
    "name": "Estat Auction",
    "application": True,
    "description": "Specific Real Estate Auction Module",
    "depends": ["estate", "website", "mail", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_templates.xml",
        "data/cron.xml",
        "views/estate_templates.xml",
        "data/website_menu.xml",
        "views/estate_property_offer.xml",
        "views/estate_property_views.xml",
    ],
    "installable": True,
    "author": "Maram-Odoo",
    "license": "LGPL-3",
}
