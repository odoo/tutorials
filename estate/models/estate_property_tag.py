from odoo import fields, models  # type: ignore


class RealEstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _check_tag_name = models.Constraint(
    'UNIQUE(name)',
    'The tag name must be unique.')
