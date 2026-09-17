from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name: str = "estate.property.tag"
    _description: str | None = None

    name: fields.Char = fields.Char()
