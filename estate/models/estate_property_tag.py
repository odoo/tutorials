from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'All the tags must be unique')
    ]

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
