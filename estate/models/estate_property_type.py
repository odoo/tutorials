from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offers_count", string="Offers")

    _unique_name = models.Constraint("UNIQUE(name)", "The Name must be Unique")

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        self.offer_count = len(self.offer_ids)
