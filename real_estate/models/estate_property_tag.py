from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color") 
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property tag name must be unique')
    ]

