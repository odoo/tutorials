from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags for Real Estate App"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ("unique_property_tag", "UNIQUE(name)", "Property Tags must be unique")
    ]
