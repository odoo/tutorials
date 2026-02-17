from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is my third model"

    name = fields.Char(required=True)
