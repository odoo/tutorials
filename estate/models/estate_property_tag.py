from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate properties Tags"

    name = fields.Char('Name', required=True, translate=True)

    _tags_uniq = models.Constraint(
        'unique(name)',
        "The tag name already exists",
    )
