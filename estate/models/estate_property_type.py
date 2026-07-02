from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate_property_type_model"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        comodel_name="estate_property_model",
        inverse_name="property_type_id",
        string="Properties"
    )