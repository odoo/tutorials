from odoo import fields,models
from datetime import timedelta


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char(required=True)
    # property_ids = fields.One2many('estate_property','property_type_id')



    
