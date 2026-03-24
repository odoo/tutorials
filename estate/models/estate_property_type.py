from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property types"
    _order = "name"
    
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'UNIQUE(name)',
        "The name of property type must be unique.",
    )

    property_ids = fields.One2many('estate.property','property_type_id')
    

