from odoo import api, fields, models 
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):

    _inherit='estate.property.offer'

    is_auction_offer_field = fields.Boolean(compute='_compute_is_auction_offer')

    def _compute_is_auction_offer(self):
        for record in self:
            record.is_auction_offer_field = record.property_id.auction_type == 'auction'
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_offer = vals.get('price')
            if property_id:
                property = self.env['estate.property'].browse(property_id)

                if property.auction_type == 'regular':
                    return super().create(vals_list)
                else:
                    if new_offer < property.expected_price:
                        raise UserError("Auction offers must be at least the expected price.")

                property.state = 'offer_received'

        return models.Model.create(self,vals_list) 
