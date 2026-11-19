from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "What kind of estate property"

    name = fields.Char('Name', required=True, translate=True)

    _unique_name = models.Constraint('UNIQUE(name)', 'Property type name must be unique.')
