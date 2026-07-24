from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Table for type of property"

    name = fields.Char(required=True)
    _check_name = models.Constraint("UNIQUE(name)", "Le nom du type doit être unique")
