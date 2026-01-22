from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Property Type", required=True)

    _check_type_uniqueness = models.Constraint(
        'unique(name)',
        'This type is already used, please use it or add a new type'
    )
