from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The property type name must be unique.')
    ]
