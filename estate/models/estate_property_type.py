from odoo import fields, models


class propertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Real Estate Properties"

    name = fields.Char(required=True)
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Name"
    )
