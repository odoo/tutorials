from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "All property tag"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    _check_tag_name = models.Constraint(
        'UNIQUE (name)',
        "The tag name must be unique."
    )
