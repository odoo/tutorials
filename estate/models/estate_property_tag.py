from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _sql_constraints = [('unique_property_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')]
