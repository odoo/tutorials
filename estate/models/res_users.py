from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Properties",
        comodel_name='estate.property',
        inverse_name='salesperson_id',
        help="Properties owned by the user.",
        domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')],
    )
