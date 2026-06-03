from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    _unique_property_tag = models.Constraint(
        'UNIQUE (name)',
        'The Property Tag must be Unique',
    )

    name = fields.Char(
        string='Tag Name',
        required=True
    )
    color = fields.Integer(string="Color")
