from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Define tags for properties"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        'UNIQUE (name)',
        'The tag name must be unique.',
    )
