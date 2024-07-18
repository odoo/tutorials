from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"  

    color = fields.Integer('Color')

    
class PropertyTag(models.Model):
    _name = 'property.tag'
    name = fields.Char(string='Tag Name')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property tag name must be unique'),
    ]
