from odoo import fields, models


class PropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type model"

    name = fields.Char(required=True)
