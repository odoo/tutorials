from odoo import models,fields
from random import randint


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order= "name asc"

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer( string="Color Index", default=lambda self: self._default_color())

    def _default_color(self):
        return randint(1, 11)

    



    _sql_constraints = [
            ('uniq_name', 'unique(name)' ,'Property Tag Name should be unique'),
        ]
    
    
    
    
    
    
    