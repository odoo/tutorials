from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order = 'name asc'
    _description = 'Tag modelisation'
    _sql_constraints = [('unique_name', 'unique(name)', 'Tag name must be unique')]

    name = fields.Char(required=True, string='Tag Name')
    color = fields.Integer(string='Color Index')
