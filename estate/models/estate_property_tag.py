from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char("Tag", required=True)
    color = fields.Integer("Color")

    _check_name = models.Constraint("UNIQUE(name)", "Tag already exists")
