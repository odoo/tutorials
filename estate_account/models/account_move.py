from odoo import fields, models


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    estate_property_id = fields.Many2one('estate.property', string="Sold Item")
