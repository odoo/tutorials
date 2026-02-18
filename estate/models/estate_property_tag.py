from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is my third model"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of the tag should be unique!',
    )
