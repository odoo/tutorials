from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "real estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "unique( name )", "Property type must be unique.")
    ]
