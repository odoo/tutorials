from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "These are Estate Module Property Tags"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property tag name must be unique"),
    ]

    name = fields.Char(string="Name", required=True)
