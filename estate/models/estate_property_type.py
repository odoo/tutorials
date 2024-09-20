from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name"

    name = fields.Char("Name", index=True, translate=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    offer_ids = fields.One2many(related="property_ids.offer_ids")
    offer_count = fields.Integer("Offer count", compute="_compute_offer_count")
    sequence = fields.Integer("Sequence", default=1, help="Used to order estate property types")


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
