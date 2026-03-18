from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Loại bất động Sản"

    name = fields.Char(string="Title", required=True)