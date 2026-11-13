from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _name_unique = models.UniqueIndex(
        "(LOWER(name))",
        "the tags should be unique (case-insensitive)!",
    )
