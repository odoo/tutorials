from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required = True)

    sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The property type name must be unique."),
    ]
