from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tags"
    name = fields.Char("Name")

    _sql_constraints = [
        ('property_tag_name_unique', 
         'UNIQUE(name)', 
         'The property tag name must be unique.')
    ]
