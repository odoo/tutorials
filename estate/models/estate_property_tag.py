from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'The name of the tag must be unique.')
    ]
