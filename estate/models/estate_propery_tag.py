from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Defines the property tags'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [('unique_name',
                        'unique(name)', 'Tag Name must be unique')]
