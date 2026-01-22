from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"

    # === FIELDS ===#

    name = fields.Char(
        required=True)
