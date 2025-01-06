from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char("Name")
    color = fields.Integer("Color")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'the property tag name must be unique.')
    ]
