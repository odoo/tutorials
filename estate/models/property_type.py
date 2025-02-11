from odoo import fields,models

class PropertyType(models.Model):
    _name= "property.type"
    _description= 'Property Type'
    name=fields.Char("Name")
    property_ids = fields.One2many("estate.property","property_type_id", string ="Property Types")

    _sql_constraints = [
        ('property_type_name_unique', 
         'UNIQUE(name)', 
         'The property type name must be unique.')
    ]
