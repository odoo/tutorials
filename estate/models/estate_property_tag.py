from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name"
    
    name = fields.Char(string='Property Tag', required=True)
    sequence = fields.Integer('Sequence', default=1)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]
