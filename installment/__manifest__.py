{
    "name": "Subscription Installment",
    "version": "1.0",
    "license": "LGPL-3",
    "category": "Subscription Installment",
    "summary": "Subscription Installment",
    "depends": ["base_setup", "sale_subscription", "documents"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_button_emi_views.xml",
        "wizard/res_setting_config.xml",
        "wizard/inherit_subscription.xml",
        "data/master_data.xml",
        "data/cron.xml",
    ],
    "installable": True,
    "application": True,
}
