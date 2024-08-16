from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate property tag"
    name = fields.Char('Title', required = True) 
    _order = "name"
    color = fields.Integer("Color")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]