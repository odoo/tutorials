from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'Property type name must be unique.',
    )
