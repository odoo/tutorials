from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char('Type', required=True)
    description = fields.Text()

    _unique_type = models.Constraint(
        'UNIQUE(name)',
        'Property type name exists'
    )
