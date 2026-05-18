from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Tag'
    _order = "name"

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer()

    _unique_tag_name = models.Constraint(
        'unique(name)',
        'The property tag name must be unique.'
    )
