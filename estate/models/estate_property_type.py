from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types for our properties'

    name = fields.Char(required=True)
    
        #region Constraint
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The property type names MUST be unique.'),
    ]

    #endregion
