from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'property tags'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Tag name must be unique')
    ]
    _order = 'name'
    name = fields.Char(required = True)
    color = fields.Integer()