from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _check_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name should be unique.',
    )
