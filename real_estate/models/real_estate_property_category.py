from odoo import fields, models

class RealEstateCategory(models.Model):
    _name = "real.estate.property.category"
    _description = "Table for Categories of properties"

    name = fields.Char(string = 'Category', required = True)
