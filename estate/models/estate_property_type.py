from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"
    _order = "name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer count", compute="_compute_offer_count")

    _name_unique = models.Constraint("unique (name)", "The name must be unique")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
