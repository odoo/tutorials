from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char()
    color = fields.Integer(string='Color', help='Color Index for the Tag')

    _sql_constraints = [
        ('check_tag_unique','UNIQUE(name)','The name must be unique'),
    ]
