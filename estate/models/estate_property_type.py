from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _rec_name = "bedrooms"

    name = fields.Char(string="Property Type", required=True)
    bedrooms = fields.Char(string="Bedrooms", required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )
