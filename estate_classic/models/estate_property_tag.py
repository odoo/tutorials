from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate_classic.property.tag"
    _description = "Property tag for an estate"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("unique_name", "UNIQUE (name)", "You cannot have two property tags with the same name.")
    ]
