# estate/models/estate_property_tag.py
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Tag name must be unique."),
    ]
    _order = "name"
    color = fields.Integer("Color")
    name = fields.Char(required=True)