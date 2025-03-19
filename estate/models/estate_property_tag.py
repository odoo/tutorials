from odoo import fields, models 


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name desc" 

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color") 

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]
