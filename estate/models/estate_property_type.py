from odoo import fields, models


class EstatePropertyTyoe(models.Model):
    _name = "estate.property.type"
    _description = "Model containing property type"

    name = fields.Char(required=True, default="Unknown")
