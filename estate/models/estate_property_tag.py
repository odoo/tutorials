from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_tag_name", "UNIQUE(name)", "The tag name must be unique")
    ]
