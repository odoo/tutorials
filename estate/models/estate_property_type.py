from odoo import models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "listing for property types"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]
