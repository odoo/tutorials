from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color") 

    _sql_constraints = [
        ('check_unique_property_tag', 'UNIQUE(name)', 
         'A property tag must be unique.')
    ]
    
