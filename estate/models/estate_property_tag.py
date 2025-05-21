from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property tag name must be unique')
    ]
