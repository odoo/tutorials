from odoo import fields, models


class InheritedUser(models.Model):
    _inherit= "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", domain=lambda self: [("state", "in", ("new", "offer_received"))])
