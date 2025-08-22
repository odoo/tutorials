from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [("unique_type", "UNIQUE(name)", "Type name must be unique")]
