from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('property_tag_name_unique', 'UNIQUE(name)', 'Property tag name must be unique')
    ]
