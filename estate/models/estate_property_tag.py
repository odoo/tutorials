from odoo import fields , models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for property tags"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 
         'Property tag name must be unique.')
    ]
