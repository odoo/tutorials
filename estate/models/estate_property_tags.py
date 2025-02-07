from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Tags for Property"

    name = fields.Char(string="Property Tag", required=True)

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]

    
