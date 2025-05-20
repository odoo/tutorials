from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A tag used to describe a property"

    name = fields.Char(required=True)
