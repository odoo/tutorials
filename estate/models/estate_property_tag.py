from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag model"

    # === FIELDS ===#

    name = fields.Char(
        required=True)
