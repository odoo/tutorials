from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag to be applied to a property"

    name = fields.Char(required=True)
