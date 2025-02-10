from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is the model for the estate property type"

    name = fields.Char(string="Name", required=True)
