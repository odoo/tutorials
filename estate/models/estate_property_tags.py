from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Tags t apply to real estate properties"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tags must be unique')
    ]