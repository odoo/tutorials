from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Adds different property tags"
    name = fields.Char(required=True)
