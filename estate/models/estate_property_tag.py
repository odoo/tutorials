from odoo import fields, models


class propertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the Real Estate Property"

    name = fields.Char(required=True)
