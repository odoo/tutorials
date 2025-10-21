from odoo import fields, models


class PropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag model"

    name = fields.Char(required=True)
