from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = "Real Estate Tag"

    name = fields.Char(string="Label", required=True)
    color = fields.Integer(string="Color")
