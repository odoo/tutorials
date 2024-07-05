from odoo import models, fields


class Estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(required=True)
    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type"
    )
