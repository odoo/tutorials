from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real Estate Property Types"

    name = fields.Char(required=True)