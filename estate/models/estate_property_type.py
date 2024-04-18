from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"

    name = fields.Char(string="Type", required=True)
