from odoo import fields, models
from odoo.api import depends


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "a type of property"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", "Offer")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)

    _sql_constraints = [("unique_name", "unique (name)", "A type with this name already exist.")]
