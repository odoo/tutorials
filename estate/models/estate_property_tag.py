from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate property tag module'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'The tag name must be unique'),
    ]
