from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type model"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
