from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    estate_property_id = fields.Many2one(
        string="Estate Property",
        help="The estate property related to this account move.",
        comodel_name="estate.property"
    )
