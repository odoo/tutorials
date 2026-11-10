from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
    _name_unique = models.Constraint("unique(name)", "Tag name must be unique")
    _order = "name"
