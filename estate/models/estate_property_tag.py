from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.tag"
    _order = "name"
    _description = "Real_Estate property model"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Already exist.')
     ]
