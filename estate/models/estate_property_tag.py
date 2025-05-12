from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name asc"
    
    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color")
    
    # SQL Constraints
    
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]
    