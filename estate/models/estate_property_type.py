from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This contains information of properties by its type."

    name = fields.Char(string = "Name", required = True)
