from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for real estate properties"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tag name already exists!"),
    ]
