from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of properties"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_tag = models.Constraint(
        'unique(name)',
        'The tag name must be unique',
    )
