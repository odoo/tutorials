from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "realestate.properties.type"
    _description = "Real estate property type"

    property_type_id = fields.Char("Property type", required=True)
