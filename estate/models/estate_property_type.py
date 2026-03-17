from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate system - Property Type"

    name = fields.Char(string="Property Type Name", required=True)
