
from odoo import models, fields

class estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"

   
    name = fields.Char(required=True)