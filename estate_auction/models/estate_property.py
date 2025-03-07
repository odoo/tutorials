from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class EstatePropertyAuction(models.Model):
    _inherit = "estate.property"

    selling_method = fields.Selection(
        [
            ('regular', 'Regular Sale'),
            ('auction', 'Auction')
        ],
        string="Selling Method",
        default='regular',
    )
    auction_end_time = fields.Datetime(string="Auction End Time")
    highest_offer = fields.Float(string="Highest Offer", readonly=True)
    highest_bidder = fields.Many2one("res.partner", string="Highest Bidder", readonly=True)
    auction_state = fields.Selection(
        string="Auction State",
        help="State of the auction",
        selection=[
            ('template', 'Template'),
            ('auction', 'Auction'),
            ('sold', 'Sold'),
        ],
        default='template',
        copy=False,
        tracking=True
    )

    @api.onchange('selling_method')
    def _onchange_selling_method(self):
        if self.auction_state == 'auction' and self.selling_method != 'auction':
            raise UserError("You cannot switch to Regular Sale after the auction has started.")   
                 
    def _cron_accept_highest_offer(self):
        """Automatically accept the highest offer when the auction ends."""
        now_utc = datetime.now()

        expired_auctions = self.search([
            ("auction_end_time", "<=", now_utc),
            ("auction_state", "=", "auction"),
        ])

        for property in expired_auctions:

            offers = property.offer_ids.sorted("price", reverse=True)

            if offers:
                highest_offer = offers[0]  
                if property.auction_state != "sold":
                    highest_offer.write({"status": "accepted"})
                    property.write({
                        "highest_offer": highest_offer.price,
                        "highest_bidder": highest_offer.partner_id.id,
                        "buyer_id": highest_offer.partner_id.id,
                        "auction_state": "sold",
                        "state": "offer_accepted",
                    })
                    template = self.env.ref('estate_auction.email_template_offer_accepted')
                    if template:
                        template.send_mail(highest_offer.property_id.id, force_send=True)

                    lower_offers = offers[1:]
                    if lower_offers:
                        lower_offers.write({"status": "refused"})
                        template_rejected = self.env.ref('estate_auction.email_template_offer_rejected')
                        for offer in lower_offers:
                            if template_rejected:
                                template_rejected.send_mail(offer.property_id.id, force_send=True)
                    property.message_post(body=f"Auction ended. Highest offer of {highest_offer.price} accepted automatically.")
        return True
   
    def action_start_auction(self):
        """Start the auction when the button is clicked"""
        for record in self:
            if record.selling_method != 'auction':
                raise UserError("Auction can only be started if the selling method is 'Auction'.")

            if record.auction_state == 'auction':
                raise UserError("Auction has already started!")

            if not record.auction_end_time:
                raise UserError("Please set an Auction End Time before starting the auction.")

            if record.auction_end_time <= datetime.now():
                raise UserError("Auction End Time must be in the future.")

            record.auction_state = 'auction'
