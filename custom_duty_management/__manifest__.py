{
    "name": "Custom Duty Management",
    "description": "Custom duty management for Import/Export",
    "license": "LGPL-3",
    "depends": [
        "account",
        "accountant",
        "base",
        "l10n_in",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/bill_entry_wizard_view.xml",
        "views/res_config_settings_view.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "auto_install": True,
    "application": True,
}
