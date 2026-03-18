from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The types available for properties/real estates'
    _check_name = models.Constraint('UNIQUE(name)', 'Property type name must be unique')

    name = fields.Char('Name', required=True)
