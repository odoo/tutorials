from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char("Name", required=True)

    _check_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name should be unique.',
    )
