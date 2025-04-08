from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag to describe an Estate Property'
    _sql_constraints = [
        (
            'estate_property_tag_name_unique',
            'UNIQUE(name)',
            'The tag names must be unique.',
        )
    ]

    name = fields.Char(string='Name', required=True)
