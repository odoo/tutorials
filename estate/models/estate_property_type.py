from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "property types"

    name = fields.Char('name', required=True)
