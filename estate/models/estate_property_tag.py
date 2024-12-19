from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for real state properties'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'Tag names MUST be unique.'),
    ]
