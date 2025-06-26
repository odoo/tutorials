from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    automatic_send_invoice_days = fields.Integer(
        related="company_id.account_tax_periodicity_reminder_day",
        readonly=False,
        config_parameter="invoice_send_automatic.automatic_send_invoice_days",
    )
