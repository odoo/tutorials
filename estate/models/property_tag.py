from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Tags for Properties"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_expected_price', 'UNIQUE(name)', "This tag already exists")
    ]
