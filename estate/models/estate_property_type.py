from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Property Types"

    name = fields.Char("Name", required=True)
