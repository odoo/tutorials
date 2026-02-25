from odoo import fields, models


class EstatePropertytTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate_property_tag'

    name = fields.Char(required=True)
