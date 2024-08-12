from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This property tag already exists.'),
    ]
