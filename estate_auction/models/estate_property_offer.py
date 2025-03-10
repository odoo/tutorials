from odoo import api, fields, models 
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):

    _inherit='estate.property.offer'

    is_auction_available = fields.Boolean(compute='_compute_is_auction')

    def _compute_is_auction(self):
        for record in self:
            record.is_auction_available =record.property_id.selling_method == 'auction'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_offer = vals.get('price')
            if property_id:
                property = self.env['estate.property'].browse(property_id) 
                if property.selling_method == 'regular':
                    return super().create(vals_list)
                else:
                    if property.expected_price > float(new_offer):
                        raise UserError(f"Offer must be higher then expected price {property.expected_price}")
                property.state = 'offer_received'
        return models.Model.create(self,vals_list) 
