from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the property"

    name = fields.Char(required=True)
    