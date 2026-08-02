from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True)

    color = fields.Integer()

    _uniq_name = models.Constraint(
        'unique(name)',
        'The name must be unique',
    )
