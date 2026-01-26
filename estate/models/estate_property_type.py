from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    # constraints
    _unique_type = models.Constraint(
        'UNIQUE(name)',
        'Type name should be unique'
    )

    name = fields.Char(string="Name", required=True)
