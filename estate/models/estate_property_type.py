from odoo import models,fields

class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description="Hello"

    name=fields.Char(string="Type",required=True)
