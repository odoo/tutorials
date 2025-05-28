from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    property_id = fields.Many2one(comodel_name='estate.property', string="Property")
