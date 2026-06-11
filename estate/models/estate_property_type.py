from odoo import fields, models # pylint: disable=import-error


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char(required=True)
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )

