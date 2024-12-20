from odoo import models, fields


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    estate_property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
