from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Property Tag", required=True)

    _check_tag_uniqueness = models.Constraint(
        'unique(name)',
        'This tag is already used, please use it or add a new tag'
    )
