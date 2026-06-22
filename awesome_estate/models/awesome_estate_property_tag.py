from odoo import fields, models


class AwesomeEstatePropertyTag(models.Model):
    _name = 'awesome.estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
