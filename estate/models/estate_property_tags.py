from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tags"

    name = fields.Char(required=True)
