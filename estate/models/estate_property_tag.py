from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="name", required=True)
    color = fields.Integer(string="color")

    _check_name = models.Constraint(
        "UNIQUE (name)", "Please give different tag as it is taken"
    )
