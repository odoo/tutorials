from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char()
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The property tag must be unique.")
    ]
