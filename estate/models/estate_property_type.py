from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type"
    _order = "sequence, name"

    name = fields.Char("Type", required=True)
    sequence = fields.Integer("Sequence")

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")
    _check_tag_name = models.Constraint("unique(name)", "Type should be unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
