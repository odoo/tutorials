from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for our properties'

    name = fields.Char(required=True)
    
    #region Constraint
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The property tag names MUST be unique.'),
    ]

    #endregion
    