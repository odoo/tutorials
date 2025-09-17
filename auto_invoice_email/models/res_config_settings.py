
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    send_email_invoice_days = fields.Integer(string="Send invoice by email", config_parameter="send_email_invoice_days")
