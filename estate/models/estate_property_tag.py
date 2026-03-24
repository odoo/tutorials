from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate property tags"

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The name of property tag must be unique.',
    )
    

