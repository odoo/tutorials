from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"
    
    name = fields.Char("Tag Name", required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The tag name must be unique."),
    ]

