from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = "estate_property_tag"
    _description = "The tag of an estate"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique',
    )
