from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique.")
    ]
