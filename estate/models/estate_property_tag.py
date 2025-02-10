from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"

    name = fields.Char(required = True)

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property Tag name must be unique.')
    ]
