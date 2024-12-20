from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True, trim=True)
    color = fields.Integer(string="Color", default=1)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Tag name must be unique!"),
    ]
