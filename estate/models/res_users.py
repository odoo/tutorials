from odoo import models, fields

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="property_seller_id", domain=[("state", "in", ["new", "offer received"])])
