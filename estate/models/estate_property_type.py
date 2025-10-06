from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types for Real Estate App"
    _order = "sequence , name"

    name  = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order property types"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_ids")

    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)", "Property Type names must be unique")
    ]

    @api.depends("offer_ids")
    def _compute_offer_ids(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
