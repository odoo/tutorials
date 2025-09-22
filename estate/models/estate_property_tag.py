from odoo import fields, models


class RealEstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_tag_name = models.Constraint("UNIQUE(name)", "The tag name must be unique.")
