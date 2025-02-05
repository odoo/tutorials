from odoo import fields, models

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Test Property"
    name = fields.Char(required=True)
    color = fields.Integer(string='color')
    _sql_constraints = [
        ('unique_tag_name', 
         'UNIQUE(name)', 
         'The property tag name must be unique!')
    ]
    _order = "name"
    