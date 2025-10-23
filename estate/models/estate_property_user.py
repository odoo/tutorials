from odoo import fields, models


class PropertyUser(models.Model):
    _inherit = "res.users"
    _description = "Property User"

    property_ids = fields.One2many("estate.property", "salesperson_id", domain=[('state', 'in', ('new', 'offer_received'))])
