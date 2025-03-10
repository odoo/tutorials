from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tags", required=True)
    color = fields.Integer(string="Color") 

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name should be unique.')
    ]
