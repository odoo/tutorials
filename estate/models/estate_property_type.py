from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint('UNIQUE(name)', "The type name must be unique.")
