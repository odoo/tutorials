from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "This table contain the types of tags"

    name = fields.Char(required=True)
