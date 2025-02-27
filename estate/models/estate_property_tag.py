from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for real estate properties"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tag name already exists!"),
    ]
