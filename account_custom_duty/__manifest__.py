# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Custom Duty",
    'version': "1.0",
    'description': "Import-Export Custom duty",
    'category': "Accounting/Import Exports",
    'depends': [
        "l10n_in",
        "account",
        "accountant"
    ],
    'data': [
        "security/ir.model.access.csv",
        "wizard/account_custom_duty_wizzard.xml",
        "views/res_config_settings_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": True,
    'license': "LGPL-3",
}
