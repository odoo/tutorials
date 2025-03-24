from odoo import fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_first_record(self, model_name, domain=None):
        return self.env[model_name].search(domain, limit=1).id if self.env[model_name].search(domain, limit=1) else False

    account_custom_duty = fields.Boolean(
        string="Import-Export Custom Duty"
    )
    account_import_journal_id = fields.Many2one(
        "account.journal",
        string="Import Default Journal",
        domain=[("type", "=", "general")],
        default=lambda self: self._get_first_record("account.journal", [("type", "=", "general")])
    )
    account_import_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Import Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        default=lambda self: self._get_first_record("account.account", [("account_type", "=", "expense")])
    )
    account_import_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Import Default Tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", True)],
        default=lambda self: self._get_first_record("account.account",
                                                    [
                                                        ("account_type", "in", ("asset_current", "liability_current")),
                                                        ("reconcile", "=", True)
                                                    ])
    )
    account_export_journal_id = fields.Many2one(
        "account.journal",
        string="Export Default Journal",
        domain=[("type", "=", "general")],
        default=lambda self: self._get_first_record("account.journal", [("type", "=", "general")])
    )
    account_export_custom_duty_account_id = fields.Many2one(
        "account.account",
        string="Export Custom Duty Account",
        domain=[("account_type", "=", "expense")],
        default=lambda self: self._get_first_record("account.account", [("account_type", "=", "expense")])
    )
    account_export_default_tax_account_id = fields.Many2one(
        "account.account",
        string="Export Default Tax Account",
        domain=[("account_type", "in", ("asset_current", "liability_current")), ("reconcile", "=", True)],
        default=lambda self: self._get_first_record("account.account",
                                                    [
                                                        ("account_type", "in", ("asset_current", "liability_current")),
                                                        ("reconcile", "=", True)
                                                    ])
    )
