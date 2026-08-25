from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _check_unique_tag_name = models.Constraint('unique(name)',
                                               "You cannot add a new tag with a duplicate name")
