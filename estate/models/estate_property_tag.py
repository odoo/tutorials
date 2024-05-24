from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "estate properties tags"
    _sql_constraints = [('unique_name', 'UNIQUE(name)', "Tag name must be unique")]
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
