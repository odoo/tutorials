from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [('name', 'unique(name)', 'Property type name must be unique')]
