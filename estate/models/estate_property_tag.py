from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "An estate property tag"

    name = fields.Char(required=True)
