from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate"

    name = fields.Char(required=True)
