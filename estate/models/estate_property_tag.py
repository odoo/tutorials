from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("unique_name_field", "UNIQUE(name)", "The name must be unique."),
    ]
