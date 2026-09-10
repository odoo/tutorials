from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "It is a estate property tag model"

    name = fields.Char(required=True)
