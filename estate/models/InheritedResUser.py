from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.user"

    property_ids = fields.One2many("estate.property", "user_id", "Property Id")
    