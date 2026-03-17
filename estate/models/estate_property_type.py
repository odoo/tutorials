from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "estate property"

    name = fields.Char(required=True)
