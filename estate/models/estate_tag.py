from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "A tag assocated with a property"
    _order = "name"

    _sql_constraints = [
        ("check_name", "unique(name)", "A property tag's name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
