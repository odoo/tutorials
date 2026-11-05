from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "It is a estate property tag model"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _unique_tag_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")
