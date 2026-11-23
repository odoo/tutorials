from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag with this name already exists.',
    )
