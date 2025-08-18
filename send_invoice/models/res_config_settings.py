from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    send_invoice_via_email = fields.Integer(String="send invoice by email", config_parameter="send_invoice.send_invoice_via_email"
)
