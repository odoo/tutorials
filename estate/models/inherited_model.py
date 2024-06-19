from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many("estate.property", "salesman_id", domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")