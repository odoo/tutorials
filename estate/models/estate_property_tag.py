from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    _unique_name = models.Constraint('UNIQUE(name)', 'The name of a tag should be unique.')

    name = fields.Char(required=True)
