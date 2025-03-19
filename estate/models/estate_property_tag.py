from odoo import fields, models


class PropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags attached to properties'    

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_tag', 'unique(name)', 'Property tag must be unique'),
    ]