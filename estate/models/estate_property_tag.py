from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this is property tag model"

    name = fields.Char("tag", required=True)
    _check_unique_propertyTag = models.Constraint(
        'UNIQUE(name)', "The Property tag must be unique"
    )
