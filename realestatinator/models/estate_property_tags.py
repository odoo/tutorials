from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'estate property tag'
    _order = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE (name)', 'make sure tag name is unique.')
    ]    
    

    color = fields.Integer('Colour')
    name = fields.Char('Name', required=True)
