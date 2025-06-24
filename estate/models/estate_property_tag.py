from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Store Real Estate Properties Tags"
    _order = "name"
    # SQL Constraints
    _sql_constraints = [("unique_name", "UNIQUE(name)", "The tag must be unique.")]

    name = fields.Char("Estate Type Tag", required=True, translate=True)
    color = fields.Integer("Color")