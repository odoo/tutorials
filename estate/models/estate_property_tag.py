from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _sql_constraints = [("check_unique", "UNIQUE(name)", "There is already a tag with this name.")]
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer("Color", default=0)
