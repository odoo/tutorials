from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char()

    _sql_constraints = [
        ('check_tag_unique','UNIQUE(name)','The name must be unique'),
    ]
