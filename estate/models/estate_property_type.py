from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate property"
    _unique_name = models.Constraint("UNIQUE(name)", "The name must be unique")

    name = fields.Char(required=True)
