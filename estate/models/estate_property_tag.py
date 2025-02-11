from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = 'name'
    
    _sql_constraints =[
        ('_unique_name','UNIQUE(name)','Tags must be unique'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
