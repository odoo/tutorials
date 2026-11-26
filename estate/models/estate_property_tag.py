from odoo import models, fields


class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The Property Tag name must be Unique!'
    )
