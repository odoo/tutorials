from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"

    name = fields.Char(required = True)

    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The property tag name must be unique."),
    ]
