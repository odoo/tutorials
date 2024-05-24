from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "description"

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'A property tag name and property type name must be unique.',
        )
    ]
