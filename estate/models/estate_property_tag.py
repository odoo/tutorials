from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char()
    color = fields.Integer()
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The property tag must be unique.")
    ]
