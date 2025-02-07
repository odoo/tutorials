from odoo import fields, models


class EstatePropertyTypesModel(models.Model):
    _name = "estate.property.types"
    _description = "The estate property types model"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "")
    sequence = fields.Integer(default=1, help="used for manual ordering")

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "The property type must be unique")
    ]
