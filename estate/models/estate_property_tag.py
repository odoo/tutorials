from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.',
    )
