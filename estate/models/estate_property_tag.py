from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _order = 'name'

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The property tag name must be unique.")
    ]
