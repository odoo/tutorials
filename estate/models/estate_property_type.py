
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of a property"

    name = fields.Text(required=True)
