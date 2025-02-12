from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char(required = True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The property tag name must be unique."),
    ]
