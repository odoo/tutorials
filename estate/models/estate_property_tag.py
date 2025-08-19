from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Tag Name", required=True)
    description = fields.Text(string="Description")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A tag with same name is already exists."),
    ]
