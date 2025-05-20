from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A real estate property tag such as cozy, luxurious ..."

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer()
