from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property tags"
    _order = 'name'
    _sql_constraints = [
        ('check_name', 'unique(name)', 'Property Tag must be UNIQUE.')
    ]

    name = fields.Char(string="Name",required=True)
    color = fields.Integer("Color Index", default=0)
