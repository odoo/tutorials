from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"

    name = fields.Char(string="Tag Name", required=True)

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique!')
    ]
