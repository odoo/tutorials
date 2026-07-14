from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(string="Name", required=True)
    _name_unique = models.Constraint(
        'unique(name)',
        '2 property type names cannot be same '
    )
