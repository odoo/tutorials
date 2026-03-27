from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real estate property tags"
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _check_name = models.Constraint('UNIQUE(name)', 'Tag name must be unique')
