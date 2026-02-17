from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required=True)
    
    _check_property_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )