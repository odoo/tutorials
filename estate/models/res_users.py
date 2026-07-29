from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Properities",
        comodel_name="estate_property",
        inverse_name="salesman_id",
        domain=[("state", "in", ["new", "offer_received"])],
    )
