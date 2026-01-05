from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_duty = fields.Boolean(
        readonly=False,
        help="Enable Custom Duty.",
        related='company_id.custom_duty')

    # Import Fields
    import_journal_id = fields.Many2one(
        comodel_name='account.journal',
        readonly=False,
        related='company_id.import_journal_id')

    import_duty_account_id = fields.Many2one(
        comodel_name='account.account',
        readonly=False,
        related='company_id.import_duty_account_id',
        domain="[('account_type', '=', 'expense')]")

    import_duty_tax_account_id = fields.Many2one(
        comodel_name='account.account',
        readonly=False,
        related='company_id.import_duty_tax_account_id',
        domain="[('reconcile', '=', True), ('account_type', 'in', ('asset_current', 'liability_current'))]")

    # Export Fields
    export_journal_id = fields.Many2one(
        comodel_name='account.journal',
        readonly=False,
        related='company_id.export_journal_id')

    export_duty_account_id = fields.Many2one(
        comodel_name='account.account',
        readonly=False,
        related='company_id.export_duty_account_id',
        domain="[('account_type', 'in', ('income', 'expense'))]")

    export_duty_tax_account_id = fields.Many2one(
        comodel_name='account.account',
        readonly=False,
        related='company_id.export_duty_tax_account_id',
        domain="[('reconcile', '=', True), ('account_type', 'in', ('asset_current', 'liability_current'))]")
