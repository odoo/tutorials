from odoo import fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "typie, co ty paczysz?"
    name = fields.Char(required=True)
    _sql_constraints = [
        ("unique_name","UNIQUE(name)","Type name must be unique")
    ]
