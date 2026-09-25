from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = "estate_property_tag"
    _description = "The tag of an estate"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique',
    )
