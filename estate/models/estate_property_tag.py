from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _unique_name = models.Constraint("UNIQUE (name)", "A property tag name must be unique")
