from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order ='name'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(default=1)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property tag must be unique.')
    ]
