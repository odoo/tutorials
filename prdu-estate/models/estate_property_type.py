from odoo import fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "typie, co ty paczysz?"
    name = fields.Char(required=True)
