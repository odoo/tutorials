from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate properties tags"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _sql_constraints = [
        ("check_tag_name_unique", "UNIQUE(name)",
         "The tag name should be unique.")
    ]
