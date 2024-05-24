from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "description"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'A property tag name and property type name must be unique.',
        )
    ]
