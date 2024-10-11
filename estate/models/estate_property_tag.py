from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.'),
        ]
       
    _description = 'Property Tag'

    name = fields.Char(required=True)
