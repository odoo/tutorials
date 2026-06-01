from odoo import models, api, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    is_auction_property = fields.Boolean(compute="_compute_is_auction_property")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].search([('id', '=', vals.get('property_id'))], limit=1)
            if property_record.selling_mode == 'auction':
                if property_record.auction_state != 'in_progress':
                    raise UserError("Auction is not active.")
                existing_offers = property_record.offer_ids
                property_record.offer_ids = [(5, 0, 0)]
                records = super().create(vals_list)
                property_record.offer_ids = [(4, offer.id) for offer in existing_offers]
                for record in records:
                    record.property_id.state = 'offer_received'
                return records
        return super().create(vals_list)

    @api.depends('property_id.selling_mode')
    def _compute_is_auction_property(self):
        for record in self:
            record.is_auction_property = record.property_id.selling_mode == 'auction'
