from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    name = fields.Char("Tag", required=True)
    color = fields.Integer()

    _sql_constraints = [
        ("tag_name_unique", "unique (name)", "The tag name should be unique.")
    ]
