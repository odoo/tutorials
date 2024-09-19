from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Tag for the estates_property model (Many2Many)"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)","The tag name should be unique.")
    ]
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer(default=1)
