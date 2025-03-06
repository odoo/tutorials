from odoo import fields, models

class RealEstateTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = "Real estate Tags for Properties"

    name = fields.Char(string = "Name", required = True)