from odoo import fields, models

class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Type"

    name = fields.Char(string="Type", required=True)
