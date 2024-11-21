from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_tag_name_check', 'UNIQUE(name)',
         'Tag name should be unique.'),
    ]
