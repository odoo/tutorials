from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Each name must be unique."),
    ]
