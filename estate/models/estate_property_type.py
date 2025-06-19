from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "estate property type"
    _order = "id"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'the type name must be unique')
    ]

    name = fields.Char("Name", required=True)
