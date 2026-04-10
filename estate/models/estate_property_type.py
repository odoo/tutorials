from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    line_ids = fields.One2many(
        "estate.property",
        "property_type_id"
    )
    sequence = fields.Integer(default=1)
