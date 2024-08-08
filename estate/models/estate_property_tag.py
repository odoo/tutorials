from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property tag'
    _order = 'name'
    name = fields.Char(required=True)
    color = fields.Integer(string='Color')
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', 'Name of the Property must be unique')
    ]
