from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "real esate properties tags"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'A property tag name must be unique!'),
    ]
