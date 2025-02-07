from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags for Real Estate App"

    name = fields.Char(required=True)
