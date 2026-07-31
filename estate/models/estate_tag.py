from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag"
    _order = "name"

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        "Another tag already exists with the same name!"
    )

    name = fields.Char(string="Tag")
    color = fields.Integer()
