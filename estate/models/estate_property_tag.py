from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_unique = models.Constraint(
        'unique(name)',
        'The Property Tag must be unique.',
    )
