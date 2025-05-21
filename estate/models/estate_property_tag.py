from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "This tag already exists."),
    ]
