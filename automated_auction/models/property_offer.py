from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    is_auction = fields.Selection(related='property_id.property_auction_type')

    # CRUD
    @api.model_create_multi
    def create(self, vals_list):
        property_price_list = [] 
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals.get('property_id'))
            actual_price = vals.get('price', 0)  # Store actual offer price
            property_price_list.append(actual_price)
            vals['price'] = actual_price if actual_price > property.best_price else property.best_price + 1

        offers = super().create(vals_list)

        for offer, actual_price in zip(offers, property_price_list):
            if actual_price is not None:
                offer._generate_price(property_price_vals=actual_price)

            property = offer.property_id

            if property.property_auction_type == 'regular' and property.best_price > actual_price:
                raise UserError(_(f"A higher or equal offer already exists, increase your offer price.\n(It should be more than {property.best_price})"))
            elif property.property_auction_type == 'auction' and not property.start_time:
                raise UserError(_("Auction isn't started yet."))
            elif property.property_auction_type == 'auction' and property.end_time and property.end_time < fields.Datetime.now():
                raise UserError(_("Auction time Ended."))
            elif property.expected_price > actual_price:
                raise UserError(_("You can not add offer less than Expected price"))

            if actual_price > property.best_price:
                property.highest_offer_bidder = offer.partner_id
            property.state = 'offer_received'
        return offers

    def _generate_price(self, property_price_vals=None):
        if property_price_vals:
            self.write({'price': property_price_vals})
