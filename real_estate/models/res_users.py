from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
