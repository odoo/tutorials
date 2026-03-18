from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "A type of property"

    name = fields.Char(string='Title', required=True)
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique.'
    )
