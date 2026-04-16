from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="name", required=True)

    _check_name = models.Constraint(
        "UNIQUE (name)", "Please give different tag as it is taken"
    )
