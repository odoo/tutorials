from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags module for Odoo 19 tutorials"

    name = fields.Char(required=True, string="Tag Name")

    _check_unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.',
    )
