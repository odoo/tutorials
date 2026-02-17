from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is my second model"

    name = fields.Char(required=True)
