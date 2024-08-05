from odoo import models, fields


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string='Name', required=True)
