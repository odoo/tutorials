from odoo import fields, models


class Estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Char()
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type"
    )
