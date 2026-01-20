from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('estate.property', string="Property", readonly=True, help="Property related to this invoice")
