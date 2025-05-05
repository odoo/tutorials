# models/estate_property_tag.py
from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "The property Tag must be unique.",
        ),
    ]
