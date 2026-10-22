from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag object"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    _unique_name = models.UniqueIndex(
        '(name)',
        'name tag must be unique',
    )
