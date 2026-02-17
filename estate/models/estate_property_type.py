from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type module for Odoo 19 tutorials Hello World"

    name = fields.Char(required=True, string="Property Type Name")
