from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property (appartment, house...)"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique.")
    ]
