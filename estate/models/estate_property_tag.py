from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"

    name = fields.Char("Tag", required=True)

    _sql_constraints = [
        ("tag_name_unique", "unique (name)", "The tag name should be unique.")
    ]
