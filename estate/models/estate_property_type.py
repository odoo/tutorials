from odoo import fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Help to set type for property"

    name = fields.Char(required=True)
