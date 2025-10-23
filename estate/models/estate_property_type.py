from odoo import api, fields, models


class PropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type model"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")
    sequence = fields.Integer("Sequence")

    _check_type_uniqueness = models.Constraint(
        "UNIQUE(name)",
        "Each type should have a unique name."
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
