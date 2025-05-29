from odoo import fields, models


class ResUsers(models.Model):
    """Model extending 'res.users' model for real estate functionality.

    This model adds a relationship to the 'estate.property' model, allowing users
    (salespersons) to be associated with real estate properties they manage.
    """

    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Estate Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
