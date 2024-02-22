from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()

    _sql_constraints = [('name', 'unique(name)', 'Property tag name must be unique')]
