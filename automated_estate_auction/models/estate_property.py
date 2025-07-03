from odoo import fields, models
import datetime


class EstateProperty(models.Model):
    _inherit = "estate.property"

    property_sell_type = fields.Selection(
        [("auction", "Auction"), ("regular", "Regular")]
    )
    auction_state = fields.Selection(
        [
            ("template", "Template"),
            ("auction", "Auction"),
            ("sold", "Sold"),
        ],
        default="template",
    )
    auction_end_time = fields.Datetime(string="End Time")
    highest_offer = fields.Float(string="Highest Offer", readonly=True)
    highest_bidder = fields.Many2one(
        comodel_name="res.partner", string="Highest Bidder", readonly=True
    )

    def action_start_auction(self):
        self.auction_state = "auction"

    def method_to_check_auction_remaining_time(self):
        properties = self.env["estate.property"].search(
            [
                ("property_sell_type", "=", "auction"),
                ("auction_state", "=", "auction"),
                ("auction_end_time", "<=", datetime.datetime.now()),
            ]
        )
        for record in properties:
            record.auction_state = "sold"
            record.state = "sold"

            highest_offer_obj = None
            highest_price = 0.0

            sorted_offers = record.offer_ids.sorted(key=lambda o: o.price, reverse=True)

            if sorted_offers:
                highest_offer_obj = sorted_offers[0]
                highest_price = highest_offer_obj.price

                record.highest_offer = highest_price
                record.highest_bidder = highest_offer_obj.partner_id

                highest_offer_obj.action_accept_offer()

                for offer in sorted_offers[1:]:
                    offer.action_reject_offer()
            else:
                record.selling_price = 0.0
                record.buyer_id = False
