{
    "name": "Auto Invoice Email",
    "version": "1.0",
    "summary": "Automatically send invoices by email after configured days",
    "category": "Accounting",
    "author": "HAAHI",
    "depends": ["account"],
    "data": [
        "views/res_config_settings.xml",
        "data/cron_auto_send.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
