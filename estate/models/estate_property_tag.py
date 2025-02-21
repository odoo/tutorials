from odoo import fields
from odoo import models

class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _sql_constraints = [
        ('check_unique_property_tag', 'UNIQUE(name)', 'Property Tag already exists')
    ]
    _order = "name"
#------------------------------------------------Basic Fields-------------------------------------------#
    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="Colour Index") 

