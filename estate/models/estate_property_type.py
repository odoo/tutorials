from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Name", required=True)

    _check_name_unique = models.Constraint(
        'unique(name)',
        'Property type name must be unique.'
    )
