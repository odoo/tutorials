from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color", default="0")

    _sql_constraints = [
        ("name_unique", "unique(name)", "Name must be unique!"),
    ]
