from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    _unique_name = models.Constraint("UNIQUE (name)", "A property type should be unique")

    name = fields.Char(required=True)
