{
    "name": "Import-Export Management",
    "summary": "Manage custom duties on import & export transactions.",
    "description": """
        Enable this feature to apply custom duty on import/export transactions,
        including Bill of Entry and Shipping Bills.
    """,
    "category": "Accounting/Localization",
    "author": "Kashish",
    "version": "1.0",
    "depends": ["accountant", "l10n_in"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/import_export_wizard_view.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
