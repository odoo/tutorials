from odoo import models, fields


class Estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "APP super mega trop bien"

    name = fields.Char(required=True)
