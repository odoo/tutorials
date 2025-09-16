from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'name'
    
    name = fields.Char("Property Type", required=True)
    _unique_name = models.Constraint(
        'unique(name)',
        "Property type name must be unique.",
    )
