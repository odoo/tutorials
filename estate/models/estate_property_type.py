from builtins import len
from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property (appartment, house...)"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique.")
    ]

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties with this type")
    property_offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers on properties with this type")
    property_offer_count = fields.Integer(compute="_compute_property_offer_count")

    def _compute_property_offer_count(self):
        for record in self:
            record.property_offer_count =  len(record.property_offer_ids) or 0
