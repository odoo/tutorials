from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "This table contain the types of tags"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer(string="color")

    _name_uniq = models.Constraint(
        "unique(name)",
        "Tag name is must be Unique",
    )
