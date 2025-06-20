from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    # Reverse relation of estate.property.salesperson_id
    property_ids = fields.One2many(
        "estate.property",  # related model
        "salesperson_id",  # inverse field on estate.property
        string="Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
