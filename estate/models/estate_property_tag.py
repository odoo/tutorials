from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Define the tags of the property"

    name = fields.Char(required=True)
