from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'Tag name should be unique.')]
