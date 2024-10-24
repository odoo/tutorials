from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name asc"

    name = fields.Char(string="Title", required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color", default=1)

    _sql_constraints = [
        (
            "check_unique_name",
            "UNIQUE(name)",
            "Tag already exists.",
        ),
    ]
