from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Real Estate Property Type"
    _order = "sequence, name, id"

    name = fields.Char(required=True, string="Property Type")

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "Property type must be unique"),
    ]

    offer_ids = fields.One2many("estate.property.offers", "property_type_id")

    property_ids = fields.One2many("estate.property", "property_type_id")

    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    offer_counts = fields.Integer(compute="_compute_offers_by_property_types")

    @api.depends("offer_ids")
    def _compute_offers_by_property_types(self):
        for record in self:
            record.offer_counts = len(record.offer_ids)
