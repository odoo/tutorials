from odoo import fields, models

class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag'

    name = fields.Char(string="Name", required=True)