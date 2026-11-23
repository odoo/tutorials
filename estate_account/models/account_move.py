from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    estate_property_id = fields.Many2one(
        string="Property", comodel_name="estate.property"
    )
