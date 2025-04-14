from odoo import models, api, exceptions, fields


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    is_auction = fields.Boolean(compute="_compute_is_auction", readonly=True)

    def _compute_is_auction(self):
        for record in self:
            if record.property_id.sale_type == "auction":
                record.is_auction = True
            else:
                record.is_auction = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals['property_id'])
            if property.sale_type == 'auction':
                if vals['price'] < property.expected_price:
                    raise exceptions.UserError("Offer must be at least expected price!")
            else:
                offer_prices = property.offer_ids.mapped('price')  # list of all existing offer price
                max_price = max(offer_prices, default=0)  # fatch max price from price list and if null then 0
                offer_price = vals['price']   # price of offer which try to create
                if offer_price < max_price:
                    raise exceptions.UserError("You cannot create an offer lower than an existing offer.")

                property.write({"state": "offer_received"})

        # Finally call the original create
        return super(EstatePropertyOffer, self.with_context(isAuction=True)).create(vals_list)
