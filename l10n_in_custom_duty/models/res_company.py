from odoo import fields, models


class Company(models.Model):
    _inherit="res.company"
    
    l10n_in_custom_duty_enabled = fields.Boolean(string="Custom Import/Export Duty")
    
    # import fields
    import_custom_duty_journal_id = fields.Many2one(comodel_name="account.journal", string="Import Journal", domain=[("type", "=", "general")])
    import_custom_duty_account_id = fields.Many2one(comodel_name="account.account", string="Import Custom Duty Account", domain=[("account_type", "=", "expense")])
    import_default_tax_account_id = fields.Many2one(
        comodel_name="account.account", string="Import Default Tax Account",
        domain=[("account_type","in", ["asset_current", "liability_current"]), ("reconcile", "=", True)]
    )
    
    # export fields
    export_custom_duty_journal_id = fields.Many2one(comodel_name="account.journal", string="Export Journal", domain=[("type", "=", "general")])
    export_custom_duty_account_id = fields.Many2one(comodel_name="account.account", string="Export Custom Duty Account", domain=[("account_type", "in", ["expense", "income"])])
    export_default_tax_account_id = fields.Many2one(
        comodel_name="account.account", string="Export Default Tax Amount",
        domain=[("account_type","in", ["asset_current", "liability_current"]), ("reconcile", "=", True)]
    )
