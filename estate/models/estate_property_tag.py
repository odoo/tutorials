from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of estate are defined"
    _order = "name asc"
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', 'The name of the tag should be unique')
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
