from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Tags used to describe a property"

    name = fields.Char("name", required=True)
