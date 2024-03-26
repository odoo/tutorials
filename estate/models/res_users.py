"""child model for implementing estate related `res.users` logic"""

from odoo import fields, models


class ResUsersChild(models.Model):
    "Estate property tag odoo model"
    _inherit = "res.users"

    property_ids = fields.One2many(
            "estate.property", "salesperson_id",
            domain=[("state", "in", ["new", "offer_received"])])
