from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'The name must be unique')]
