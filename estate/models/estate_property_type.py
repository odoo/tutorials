from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model containing property type"

    name = fields.Char(required=True, default="Unknown")
