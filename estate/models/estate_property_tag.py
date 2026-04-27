from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = 'name'

    name = fields.Char(required=True)
    Color = fields.Integer(default=3)

    _unique_tag = models.Constraint(
        'unique(name)',
        'Property tag should be unique'
    )
