from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char(required = True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property Tag name must be unique.')
    ]
