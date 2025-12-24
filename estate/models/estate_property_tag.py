from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _order = 'name'

    name = fields.Char(
        "Name",
        required=True,
    )
    _name_uniq = models.Constraint(
        'unique(name)',
        'This property tag already exists.',
    )
    color = fields.Integer(
        "Color"
    )
