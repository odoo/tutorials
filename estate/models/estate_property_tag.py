from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.',
    )
