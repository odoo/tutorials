{
    "name": "Custom Duty on Import Export",
    "summary": "Manage custom duties on import & export transactions.",
    "description": "Provide functionality to handle and calculate custom duties on import and export transactions within the accounting module.",
    "category": "Accounting",
    "version": "1.0",
    "depends": ["accountant", "l10n_in"],  
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/bill_entry_wizard_view.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
