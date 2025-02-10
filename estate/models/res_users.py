from odoo import models, fields

class resUsers(models.Model):
    _inherit = "res.users"  # Extend the existing res.users model

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",         
        string="Properties",
        domain=[("state", "in", ["new", "offer_received"])]
    )
