from odoo import models, fields


class Testing_type(models.Model):
    _name = "estate.property.type"
    _description = "This is Real Estate property type"

    name = fields.Char(required=True)
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="property type"
    )
