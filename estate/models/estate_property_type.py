from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property types"

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The name of property type must be unique.',
    )
    

