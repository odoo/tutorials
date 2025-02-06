from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type model"


    name = fields.Char(string="Title", required=True)
