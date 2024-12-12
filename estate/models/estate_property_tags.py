from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property tags Table"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The property tags must be unique.")
    ]
    _order = "name"
