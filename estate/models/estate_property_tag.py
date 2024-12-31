from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The tags of real estate properties"
    _order = "name"
    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name must be unique.',
        )
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
