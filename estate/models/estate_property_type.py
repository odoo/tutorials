from odoo import models, fields


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char("Property Type Name", required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property type with the same name already exists.',
    )
