{
    "name": "estate",
    "depends": ["base", "mail"],
    "category": "tutorials",
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_view.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_menu.xml",
        "views/user_res_view.xml",
        "data/cron_deadline.xml",
        "data/cron_stale_property.xml",
        "data/mail_template.xml"
    ],
    "author": "RADHR",
    "license": "LGPL-3",
}
