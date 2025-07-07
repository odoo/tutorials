from odoo import fields, models

# Property type model for properties 
# prpoerties can be of type house, penthouse, etc.
class EstatePropertyType(models.Model):
      _name = "estate.property.type"
      _description = "Type of properties of estate model"
      name = fields.Char(required=True)