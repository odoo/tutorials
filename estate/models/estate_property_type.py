from odoo import models, fields


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The Property Type name must be Unique!'
    )
