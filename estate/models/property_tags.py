from odoo import fields, models


class PropertyTags(models.Model):
    _name = "property.tags"
    _description = "Property Tags"

    name = fields.Char(required=True)
