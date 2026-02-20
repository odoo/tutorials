from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is my third model"
    _order = "name"

    name = fields.Char(required=True, string="Tag")

    color = fields.Integer(default=0)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of the tag should be unique!',
    )
