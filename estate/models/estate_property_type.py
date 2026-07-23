from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "realestate.properties.type"
    _description = "Real estate property type"

    name = fields.Char("Property type", required=True)
    property_type_id = fields.Char("Property type id", required=True)
