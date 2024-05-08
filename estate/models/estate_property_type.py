from datetime import timedelta
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real estate property type module"

    name = fields.Char(string="Name", required=True)
