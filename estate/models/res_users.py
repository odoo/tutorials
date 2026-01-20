from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(  # Extend the res.users model by property_ids through the One2many relation
        "estate.property",
        "salesperson_id",
        string="Property",
        domain=[("estate_state", "in", ["new", "offer_received"])],  # show only available properties
    )
