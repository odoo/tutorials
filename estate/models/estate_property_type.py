from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string='Type', required=True)

    _uniq_tag = models.Constraint(
        'unique(name)',
        'Type must be unique',
    )
