from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for estate properties"

    name = fields.Char('Name')
    color = fields.Integer('Color', default=1)

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Name must be unique.'),
    ]

    _order = "name"
