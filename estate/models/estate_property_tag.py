from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"
    _order = 'name'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', "Property tag name must be unique.")
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
