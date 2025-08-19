from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    send_invoice_by_email = fields.Integer(string='Send invoice by email after (days)', config_parameter="send_invoice_email.send_invoice_by_email")
