from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "These are the tags for estate properties"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = [("uniq_tag", "unique(name)", "Tags should have a unique name")]
