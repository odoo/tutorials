from odoo import fields, models


class ResUsers(models.Model):
    """Show the available properties of each salesperson on their user."""

    _name = "res.users"
    _inherit = ["res.users"]

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Real Estate Properties",
        # Only the properties which are still available.
        domain=[("state", "in", ["new", "offer_received"])],
    )
