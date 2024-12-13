from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Tags'
    _order = 'name'

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The tag name must be unique')
    ]

    name = fields.Char()
    color = fields.Integer()