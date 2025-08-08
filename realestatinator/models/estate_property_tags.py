from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'estate property tag'
    _order = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE (name)', 'make sure tag name is unique.')
    ]	
    name = fields.Char('Name', required=True)
    color = fields.Integer('Colour')
