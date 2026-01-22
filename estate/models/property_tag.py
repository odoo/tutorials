from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'estate property tag'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color Index")

    _name_uniq = models.Constraint(
        'unique (name)',
        "A property tag name must be unique",
    )
