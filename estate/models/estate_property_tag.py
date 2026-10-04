from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        "Tag name must be unique",
    )
