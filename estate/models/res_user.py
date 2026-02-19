from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate_property", 
        "salesman_id", 
        string="My Properties", 
        domain=[("state", "in", ["new", "offer_received"])]
    )
