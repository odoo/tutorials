from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"
    _sql_constraints = [('name_unique','unique(name)',"this property tag is already exists!")]
    
    name = fields.Char(required=True)
    color = fields.Integer('Color Index') 
