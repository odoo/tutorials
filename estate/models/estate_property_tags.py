from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for Property"
    _order = "name asc"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(String="Color")

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]


