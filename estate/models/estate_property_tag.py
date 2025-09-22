from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)',
        "The tag name should be unique"
    )
