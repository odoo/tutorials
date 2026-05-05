from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    estate_property_id = fields.Many2one('estate.property', string="Estate Property")
