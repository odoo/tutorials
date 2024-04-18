from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = "estate_property_tag"
    _description = "estate property tag"

    name = fields.Char(string="Type", required=True)
