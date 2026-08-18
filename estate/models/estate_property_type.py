from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char('Type Name', required=True, translate=True)

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        'The type name must be unique'
    )
