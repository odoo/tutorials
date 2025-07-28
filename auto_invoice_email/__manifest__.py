{
    "name": "Auto Invoice Email",
    "version": "1.0",
    "summary": "Automatically send posted invoices by email after configured days",
    "category": "Accounting",
    "author": "Rohit",
    "depends": ["account"],
    "data": [
        "views/res_config_settings_views.xml",
        "data/auto_send_cron.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
