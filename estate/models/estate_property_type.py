from odoo import fields, models


class EstatePropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "The type of an estate"

    name = fields.Char(required=True)
