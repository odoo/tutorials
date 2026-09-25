from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property",
        "salesperson_id",
        string="Property",
        domain=[("state", "in", ["new", "offer_received"])],
    )
