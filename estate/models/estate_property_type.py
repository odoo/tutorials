from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate"

    name = fields.Char('Name')

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Name must be unique.'),
    ]
