from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this model defines property type"

    name = fields.Char("Type", required=True)
