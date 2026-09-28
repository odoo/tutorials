from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        "This tag name is already taken"
    )
