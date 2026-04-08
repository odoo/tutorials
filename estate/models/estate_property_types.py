from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "Real E-state Property Type"

    name = fields.Char(required=True)
