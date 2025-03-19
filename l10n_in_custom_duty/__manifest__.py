{
    "name": "Custom Duty",
    "version": "1.0",
    "description": "Enables functionality to apply custom duty on import/export transactions, including Bill of Entry and Shipping Bills",
    "category": "Accounting/Localizations/Custom Duty",
    "depends": [
        "accountant",
        "l10n_in"
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "wizard/account_move_custom_duty_views.xml",
        "views/account_move_views.xml",
        "security/ir.model.access.csv"
    ],
    "license": "LGPL-3",
    "auto_install": ["l10n_in"],
}
