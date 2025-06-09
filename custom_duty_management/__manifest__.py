{
    "name": "Custom Duty Management",
    "description": "Custom duty management for Import/Export",
    "license": "LGPL-3",
    "depends": [
        "accountant",
        "base",
        "l10n_in",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "views/res_config_settings_view.xml",
        "wizard/bill_entry_wizard_view.xml",
    ],
    "installable": True,
}
