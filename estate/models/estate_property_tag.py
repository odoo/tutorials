from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _discription = 'Estate Property Tag'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer()
