from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color')

    _uniq_tag = models.Constraint(
        'unique(name)',
        'Tags must be unique',
    )
