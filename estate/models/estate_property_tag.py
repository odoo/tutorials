from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Real Estate Property Tags"

    name = fields.Char(required=True, string="Tag Name")
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("check_tag_name", "UNIQUE(name)", "Tag name must be unique."),
    ]
