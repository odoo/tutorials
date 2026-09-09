from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(default=1)

    _unique_name = models.Constraint("UNIQUE(name)", "The Name must be Unique")
