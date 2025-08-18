import random
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True, index=True)
    property_type = fields.Char(string="Property Type")
  
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tags must be unique"),
    ]
    def _default_color(self):
        return random.randint(1, 11)
    color = fields.Integer(string="Color Index", default=_default_color)
