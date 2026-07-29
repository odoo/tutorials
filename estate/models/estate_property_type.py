from odoo import _, api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name"

    name = fields.Char("Property type", required=True)
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        _("Property name already exists. Property names must be unique."),
    )

    sequence = fields.Integer("Sequence")
    property_list_id = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offers", compute="_compute_offers_count")

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
