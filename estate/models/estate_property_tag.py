from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"
    _order = 'name'

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer()

    _tag_name_uniq = models.Constraint(
        'unique(name)',
        "The property tag name must be unique",
    )
