from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type."

    name = fields.Char('Property Type', required=True)

    ## CONSTRAINTS ##

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The type must be unique.',
    )
