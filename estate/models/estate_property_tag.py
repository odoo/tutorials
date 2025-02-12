from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer('Color Index') 
    
    _sql_constraints = [('name_unique','unique(name)',"this property tag is already exists!")]
