from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    ''' Add field send_email_days in res.config.settings model to store Days to sand invoice email '''
    _inherit = 'res.config.settings'

    send_email_days = fields.Integer(string="Send invoice by email", config_parameter='send_invoice_by_email.send_email_days')
