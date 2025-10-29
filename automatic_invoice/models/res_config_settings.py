from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_auto_invoice_sending = fields.Boolean(
        string="Send invoice by email",
        config_parameter="automatic_invoice.enable_auto_invoice_sending"
    )
    invoice_send_delay_days = fields.Integer(
        string="Duration of days after the date of invoice",
        config_parameter="automatic_invoice.invoice_send_delay_days"
    )
