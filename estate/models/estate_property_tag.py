from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Title", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [('unique_property_tag_name', 'unique(name)', 'The tag name must be unique!')]
