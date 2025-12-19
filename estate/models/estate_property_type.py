from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"

    name = fields.Char(
        "Name",
        required=True,
    )
