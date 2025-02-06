from odoo import fields, models


class EstatePropertyTypesModel(models.Model):
    _name = "estate.property.types"
    _description = "The estate property types model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "The property type must be unique")
    ]
