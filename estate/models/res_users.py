from odoo import fields, models

class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", domain="['|',('state', '=', 'new'),('state', '=', 'offer_received')]")
