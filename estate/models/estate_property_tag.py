from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
