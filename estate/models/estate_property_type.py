from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "description"

    name = fields.Char("Type", required=True)
