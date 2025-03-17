# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Custom Duty",
    'website': "https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/india.html",
    'icon': "/account/static/description/l10n.png",
    'countries': ["in"],
    'version': "1.0",
    'description': "Import-Export Custom duty",
    'category': "Accounting/Localizations/Import Exports",
    'depends': [
        "account_tax_python",
        "base_vat",
        "account",
        "l10n_in"
    ],
    'auto_install': ["account"],
    'data': [
        "security/ir.model.access.csv",
        "wizard/l10n_in_custom_duty_wizzard.xml",
        "views/res_config_settings_views.xml",
        "views/account_move_views.xml",
    ],
    'license': "LGPL-3",
}
