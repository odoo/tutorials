# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    autosend_invoices = fields.Boolean(related='company_id.autosend_invoices', readonly=False)
    days_to_send_invoice = fields.Integer(related='company_id.days_to_send_invoice', readonly=False)
